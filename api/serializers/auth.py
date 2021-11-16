from django.contrib.auth import authenticate
from django.contrib.auth import password_validation as validators
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from rest_framework.serializers import (
    EmailField,
    CharField,
    ModelSerializer,
    Serializer,
    SerializerMethodField,
    ValidationError,
)

from api.models import Institute, Student, User
from api.ses import send_email

from .user import UserSerializer


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
        user = User.objects.create(**validated_data, verified=True)
        user.set_password(validated_data["password"])

        request = self.context.get("request")
        if "HTTP_ORIGIN" in request.META:
            user.site = request.META["HTTP_ORIGIN"]
        elif "HTTP_REFERER" in request.META:
            user.site = request.META["HTTP_REFERER"]

        user.save()

        if user.is_student:
            Student.objects.create(user=user)
        elif user.is_institute:
            Institute.objects.create(user=user)

        send_email(
            user.email,
            render_to_string("email_verification/subject.txt"),
            render_to_string(
                f"email_verification/body.html",
                context={"name": user.name, "code": user.verification_code},
            ),
        )

        return user


class VerifyEmailSerializer(Serializer):
    email = EmailField()
    verification_code = CharField()

    def validate(self, attrs):
        user = User.objects.filter(email=attrs.get("email")).first()
        if not user:
            raise ValidationError(_("Invalid email id"))

        if user.verification_code != attrs.get("verification_code"):
            raise ValidationError(_("Incorrect verification code"))

        attrs["user"] = user

        return attrs

    def save(self, validated_data):
        user = validated_data.get("user")
        user.verified = True
        user.save()

        send_email(
            user.email,
            render_to_string("registration/subject.txt"),
            render_to_string(
                f"registration/{'student' if user.is_student else 'institute'}.html",
                context={"name": user.name, "title": "eTests"},
            ),
        )

        return user


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

            if not user.site:
                request = self.context.get("request")
                if "HTTP_ORIGIN" in request.META:
                    user.site = request.META["HTTP_ORIGIN"]
                elif "HTTP_REFERER" in request.META:
                    user.site = request.META["HTTP_REFERER"]
                user.save()
        else:
            msg = _("Unable to log in with provided credentials.")
            raise ValidationError(msg)

        attrs["user"] = user
        return attrs


class JWTSerializer(Serializer):
    """
    Serializer for JWT authentication.
    """

    refresh = CharField(max_length=4096, required=True, trim_whitespace=True)
    access = CharField(max_length=4096, required=True, trim_whitespace=True)

    user = SerializerMethodField()

    def get_user(self, obj):
        return UserSerializer(obj["user"], context=self.context).data


class SocialSerializer(Serializer):
    provider = CharField(max_length=255, required=True)
    access_token = CharField(max_length=4096, required=True, trim_whitespace=True)


__all__ = (
    "RegisterSerializer",
    "LoginSerializer",
    "VerifyEmailSerializer",
    "SocialSerializer",
    "JWTSerializer",
)
