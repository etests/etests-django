from datetime import date
from random import choice
from string import digits

from django import forms
from django.contrib.auth import password_validation
from django.template import loader
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from api.models import ResetCode

from .models import Payment, Image, User
from .ses import send_email
from .utils import random_key


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=_("Email"), max_length=254)

    def generate_code(self, user):
        try:
            return ResetCode.objects.get(
                user=user, done=False, date_added=date.today()
            ).reset_code
        except:
            return ResetCode.objects.create(
                user=user, reset_code=random_key(length=6)
            ).reset_code

    def get_user(self, email):
        """Given an email, return matching user who should receive a reset code.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        try:
            return User._default_manager.get(
                **{"%s__iexact" % User.get_email_field_name(): email, "is_active": True}
            )
        except:
            raise forms.ValidationError("No user with this email id.")

    def save(self, from_email):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        email = self.cleaned_data["email"]
        user = self.get_user(email)
        subject = render_to_string("password_reset/subject.txt")
        message = render_to_string(
            "password_reset/body.html",
            context={"name": user.name, "code": self.generate_code(user)},
        )
        send_email(email, subject, message, from_email=from_email)


class SetPasswordForm(forms.Form):
    """
    A form that can be used change the password without entering the old
    password
    """

    new_password = forms.CharField(
        label=_("New password"),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password(self):
        password = self.cleaned_data.get("new_password")
        password_validation.validate_password(password, self.user)
        return password

    def save(self, commit=True):
        password = self.cleaned_data["new_password"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ("file",)
