from datetime import date

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from rest_framework.serializers import (
    CharField,
    EmailField,
    Serializer,
    ValidationError,
)

from api.forms import PasswordResetForm, SetPasswordForm
from api.models import ResetCode


class PasswordResetSerializer(Serializer):
    email = EmailField()

    password_reset_form_class = PasswordResetForm

    def validate_email(self, value):
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise ValidationError(self.reset_form.errors)

        return value

    def save(self):
        request = self.context.get("request")
        self.reset_form.save(from_email=settings.EMAIL_ID)


class PasswordResetConfirmSerializer(Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """

    reset_code = CharField()
    new_password = CharField(max_length=128)

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
            raise ValidationError(self.set_password_form.errors)

        return attrs

    def save(self):
        self.reset_code_instance.done = True
        self.reset_code_instance.save()
        return self.set_password_form.save()


class PasswordChangeSerializer(Serializer):
    old_password = CharField(max_length=128)
    new_password = CharField(max_length=128)

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
            raise ValidationError(err_msg)
        return value

    def validate(self, attrs):
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )

        if not self.set_password_form.is_valid():
            raise ValidationError(self.set_password_form.errors)
        return attrs

    def save(self):
        self.set_password_form.save()
        if not self.logout_on_password_change:
            from django.contrib.auth import update_session_auth_hash

            update_session_auth_hash(self.request, self.user)
