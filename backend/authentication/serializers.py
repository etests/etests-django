from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import password_validation as validators
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpRequest
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode as uid_decoder
from django.utils.translation import ugettext_lazy as _
from requests.exceptions import HTTPError
from rest_framework import exceptions, serializers
from rest_framework.exceptions import ValidationError

from .forms import PasswordResetForm, SetPasswordForm
from api.models import ResetCode
from .models import *
from datetime import date

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "email", "phone", "password", "is_student", "is_institute")
        extra_kwargs = {"phone": {"required": False}}

    def validate_email(self, email):
        if User.objects.filter(email=email):
            raise serializers.ValidationError(
                _("A user is already registered with this e-mail address.")
            )
        return email

    def validate_password(self, password):
        errors = dict()
        try:
            validators.validate_password(password=password, user=User)
        except exceptions.ValidationError as e:
            errors["password"] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
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
    password = serializers.CharField(style={"input_type": "password"})

    def authenticate(self, **kwargs):
        return authenticate(self.context["request"], **kwargs)

    def _validate_username(self, username, password):
        user = None
        instance = (
            User.objects.filter(email=username).first()
            or User.objects.filter(phone=username).first()
        )
        if instance:
            user = self.authenticate(email=instance.email, password=password)
        else:
            msg = _("No user with this email/password.")
            raise exceptions.ValidationError(msg)

        return user

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = None

        user = self._validate_username(username, password)

        if user:
            if not user.is_active:
                msg = _("User account is disabled.")
                raise exceptions.ValidationError(msg)
        else:
            msg = _("Unable to log in with provided credentials.")
            raise exceptions.ValidationError(msg)

        attrs["user"] = user
        return attrs


class InstituteDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institute
        fields = "__all__"


class StudentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    birth_date = serializers.SerializerMethodField(read_only=True)
    pincode = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ("id", "name", "phone", "city", "state", "birth_date", "pincode")

    def get_birth_date(self, obj):
        if obj.is_student:
            return obj.student.birth_date
        return None

    def get_pincode(self, obj):
        if obj.is_institute:
            return obj.institute.pincode
        return None


class UserDetailsSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(source="*")
    details = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "name", "email", "type", "profile", "details")
        read_only_fields = ("email",)

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

    refresh = serializers.CharField()
    access = serializers.CharField()
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return UserDetailsSerializer(obj["user"], context=self.context).data


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    password_reset_form_class = PasswordResetForm

    def validate_email(self, value):
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)

        return value

    def save(self):
        request = self.context.get("request")
        self.reset_form.save(from_email=getattr(settings, "EMAIL_ID"))


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """

    reset_code = serializers.CharField()
    new_password = serializers.CharField(max_length=128)

    set_password_form_class = SetPasswordForm

    def validate(self, attrs):
        self._errors = {}

        try:
            self.reset_code_instance = ResetCode.objects.get(
                reset_code=attrs.get("reset_code"), done=False, date_added=date.today()
            )
            self.user = self.reset_code_instance.user
        except Exception as e:
            print(e)
            raise ValidationError({"reset_code": ["Invalid reset code"]})

        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)

        return attrs

    def save(self):
        self.reset_code_instance.done = True
        self.reset_code_instance.save()
        return self.set_password_form.save()


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    new_password = serializers.CharField(max_length=128)

    set_password_form_class = SetPasswordForm

    def __init__(self, *args, **kwargs):
        self.old_password_field_enabled = True
        self.logout_on_password_change = False
        super(PasswordChangeSerializer, self).__init__(*args, **kwargs)

        if not self.old_password_field_enabled:
            self.fields.pop("old_password")

        self.request = self.context.get("request")
        self.user = getattr(self.request, "user", None)

    def validate_old_password(self, value):
        invalid_password_conditions = (
            self.old_password_field_enabled,
            self.user,
            not self.user.check_password(value),
        )

        if all(invalid_password_conditions):
            err_msg = _(
                "Your old password was entered incorrectly. Please enter it again."
            )
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
