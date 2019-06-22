from django.db import models, migrations
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta

class MyUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be a staff member.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be a staff member.")
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True, blank=True, null=True)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    date_joined = models.DateField(auto_now_add=True)
    is_staff = models.BooleanField(_("staff status"), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    is_student = models.BooleanField(default=False)
    is_institute = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    objects = MyUserManager()

    def __str__(self):
        return self.name

class Institute(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pincode = models.CharField(max_length=10)

    def __str__(self):
        return self.user.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.user.is_institute = True
        super(Institute, self).save(*args, **kwargs)


class Student(models.Model):
    GENDERS = (("M", "Male"), ("F", "Female"), ("O", "Others"))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDERS)
    institute = models.ForeignKey(Institute, on_delete=models.SET_NULL, null=True)
    birth_date = models.DateField()

    def __str__(self):
        return self.user.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.user.is_student = True
        super(Student, self).save(*args, **kwargs)