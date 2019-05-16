from django.db import models, migrations
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import BaseUserManager
from django.db.models.signals import pre_save
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta

class MyUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be a staff member.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be a staff member.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length = 100, blank=False, null=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, blank=True, null=True, unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user is a staff member.'),
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    phone = models.CharField(max_length=10, blank=False, null=False, unique=True)
    state = models.CharField(max_length = 100, blank=False)
    city = models.CharField(max_length = 100, blank=False)
    date_joined = models.DateField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self):
        return self.name


@receiver(pre_save, sender=User)
def set_username(sender, instance, **kwargs):
    if not instance.username:
        username = "_".join(instance.name.split()).lower()
        counter = 1
        if User.objects.filter(username=username):
            next_username = instance.email.split('@')[0]
        else:
            next_username = username
        while User.objects.filter(username=next_username):
            next_username = username+str(counter)
            counter += 1
        instance.username = next_username

models.signals.pre_save.connect(set_username, sender=User)


class Institute(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    pincode = models.CharField(max_length=20, blank=False)


class Student(models.Model):
    GENDERS = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others'),
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    gender = models.CharField(max_length=1, choices=GENDERS)
    institute = models.ForeignKey(Institute, on_delete = models.SET_NULL, null = True)
    birth_date = models.DateField(blank=False, null=False)
