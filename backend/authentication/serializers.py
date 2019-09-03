from django.contrib.auth import get_user_model, authenticate
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode as uid_decoder
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text
import django.contrib.auth.password_validation as validators

from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError

from .models import *
from .utils import import_callable

from django.http import HttpRequest
from requests.exceptions import HTTPError

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "email", "phone", "password", "is_student", "is_institute")
        extra_kwargs = {'phone': {'required': False}}
    
    def validate_email(self, email):
        if User.objects.filter(email=email):
            raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def validate_password(self, password):
        errors = dict()
        try:
             validators.validate_password(password=password, user=User)
        except exceptions.ValidationError as e:
             errors['password'] = list(e.messages)

        if errors:
             raise serializers.ValidationError(errors)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        if user.is_student:
            Student.objects.create(user=user)
        elif user.is_institute:
            Institute.objects.create(user=user)
        return user

class VerifyEmailSerializer(serializers.Serializer):
    key = serializers.CharField()

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

    def _validate_username(self, username, password):
        user = None
        instance = User.objects.filter(email=username).first() or \
                    User.objects.filter(phone=username).first()
        if instance:
            user = self.authenticate(email=instance.email, password=password)
        else:
            msg = _('No user with this email/password.')
            raise exceptions.ValidationError(msg)
        
        return user

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = None

        user = self._validate_username(username, password)

        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs

class InstituteDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institute
        fields = '__all__' 


class StudentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__' 

class ProfileSerializer(serializers.ModelSerializer):
    birth_date = serializers.SerializerMethodField()
    pincode = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('name', 'phone', 'city', 'state', 'birth_date', 'pincode')
        
    def get_birth_date(self, obj):
        if obj.is_student:
            return obj.student.birth_date
        return None

    def get_pincode(self, obj):
        if obj.is_institute:
            return obj.institute.pincode
        return None

class UserDetailsSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(source='*')
    details = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "name", "email", "type", "profile", "details")
        read_only_fields = ('email', )

    def get_type(self, obj):
        if obj.is_student:
            return "student"
        elif obj.is_institute:
            return "institute"
        elif obj.is_staff:
            return "staff"
        return ""

    def get_details(self, obj):
        if obj.is_student:
            return StudentDetailsSerializer(obj.student, context=self.context).data
        elif obj.is_institute:
            return InstituteDetailsSerializer(obj.institute, context=self.context).data
        else:
            return None

class JWTSerializer(serializers.Serializer):
    """
    Serializer for JWT authentication.
    """
    token = serializers.CharField()
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return UserDetailsSerializer(obj['user'], context=self.context).data

class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """
    email = serializers.EmailField()

    password_reset_form_class = PasswordResetForm

    def get_email_options(self):
        """Override this method to change default e-mail options"""
        return {}

    def validate_email(self, value):
        # Create PasswordResetForm with the serializer
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)

        return value

    def save(self):
        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
        }

        opts.update(self.get_email_options())
        self.reset_form.save(**opts)

class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)
    uid = serializers.CharField()
    token = serializers.CharField()

    set_password_form_class = SetPasswordForm

    def custom_validation(self, attrs):
        pass

    def validate(self, attrs):
        self._errors = {}

        # Decode the uidb64 to uid to get User object
        try:
            uid = force_text(uid_decoder(attrs['uid']))
            self.user = User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise ValidationError({'uid': ['Invalid value']})

        self.custom_validation(attrs)
        # Construct SetPasswordForm instance
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        if not default_token_generator.check_token(self.user, attrs['token']):
            raise ValidationError({'token': ['Invalid value']})

        return attrs

    def save(self):
        return self.set_password_form.save()

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)

    set_password_form_class = SetPasswordForm

    def __init__(self, *args, **kwargs):
        self.old_password_field_enabled = getattr(
            settings, 'OLD_PASSWORD_FIELD_ENABLED', False
        )
        self.logout_on_password_change = getattr(
            settings, 'LOGOUT_ON_PASSWORD_CHANGE', False
        )
        super(PasswordChangeSerializer, self).__init__(*args, **kwargs)

        if not self.old_password_field_enabled:
            self.fields.pop('old_password')

        self.request = self.context.get('request')
        self.user = getattr(self.request, 'user', None)

    def validate_old_password(self, value):
        invalid_password_conditions = (
            self.old_password_field_enabled,
            self.user,
            not self.user.check_password(value)
        )

        if all(invalid_password_conditions):
            err_msg = _("Your old password was entered incorrectly. Please enter it again.")
            raise serializers.ValidationError(err_msg)
        return value

    def validate(self, attrs):
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )

        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        return attrs

    def save(self):
        self.set_password_form.save()
        if not self.logout_on_password_change:
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(self.request, self.user)