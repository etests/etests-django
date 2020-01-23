from django.contrib.auth import authenticate
from django.contrib.auth import password_validation as validators
from django.utils.translation import ugettext_lazy as _
from rest_framework.serializers import (
    CharField,
    ModelSerializer,
    Serializer,
    SerializerMethodField,
    ValidationError,
)

from api.models import Institute, Student, User


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "email", "phone", "password", "is_student", "is_institute")
        extra_kwargs = {"phone": {"required": False}}

    def validate_email(self, email):
        if User.objects.filter(email=email):
            raise ValidationError(
                _("A user is already registered with this e-mail address.")
            )
        return email

    def validate_password(self, password):
        errors = dict()
        try:
            validators.validate_password(password=password, user=User)
        except ValidationError as e:
            errors["password"] = list(e.messages)

        if errors:
            raise ValidationError(errors)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        if user.is_student:
            Student.objects.create(user=user)
        elif user.is_institute:
            Institute.objects.create(user=user)
        return user


class VerifyEmailSerializer(Serializer):
    key = CharField()


class LoginSerializer(Serializer):
    username = CharField()
    password = CharField(style={"input_type": "password"})

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
            raise ValidationError(msg)

        return user

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = None

        user = self._validate_username(username, password)

        if user:
            if not user.is_active:
                msg = _("User account is disabled.")
                raise ValidationError(msg)
        else:
            msg = _("Unable to log in with provided credentials.")
            raise ValidationError(msg)

        attrs["user"] = user
        return attrs


class InstituteDetailsSerializer(ModelSerializer):
    class Meta:
        model = Institute
        fields = "__all__"


class StudentDetailsSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class ProfileSerializer(ModelSerializer):
    birth_date = SerializerMethodField(read_only=True)
    pincode = SerializerMethodField(read_only=True)

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


class UserDetailsSerializer(ModelSerializer):
    profile = ProfileSerializer(source="*")
    details = SerializerMethodField()
    type = SerializerMethodField()

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


class JWTSerializer(Serializer):
    """
    Serializer for JWT authentication.
    """

    refresh = CharField()
    access = CharField()
    user = SerializerMethodField()

    def get_user(self, obj):
        return UserDetailsSerializer(obj["user"], context=self.context).data
