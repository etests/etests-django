from django.db import models, migrations
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from .utils import randomKey, unique_random_key

class MyUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email = email, **extra_fields)
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
    name = models.CharField(max_length = 100)
    email = models.EmailField(unique = True)
    phone = models.CharField(max_length = 15, unique = True, blank = True, null = True)
    state = models.CharField(max_length = 100)
    city = models.CharField(max_length = 100)
    date_joined = models.DateField(auto_now_add = True)
    is_staff = models.BooleanField(_("staff status"), default = False)
    is_active = models.BooleanField(_('active'), default = True)
    is_student = models.BooleanField(default = False)
    is_institute = models.BooleanField(default = False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    objects = MyUserManager()

    def __str__(self):
        return self.name

class Institute(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    pincode = models.CharField(max_length = 10, null = True, blank=True)
    current_credits = models.IntegerField(default = 0)
    verified = models.BooleanField(default=False)
    show = models.BooleanField(default=True)
    rating = models.FloatField(default=0)
    about = models.CharField(max_length = 1024, null = True, blank=True)

    def __str__(self):
        return self.user.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.user.is_institute = True
        super(Institute, self).save(*args, **kwargs)

class Batch(models.Model):
    joining_key = models.CharField(max_length = 8, default=randomKey)
    name = models.CharField(max_length = 100)
    institute = models.ForeignKey(Institute, related_name = "batches", on_delete = models.CASCADE)

    def students(self):
        return Student.objects.filter(enrollment__batch = self)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Batches"

class Enrollment(models.Model):
    institute = models.ForeignKey(Institute, on_delete = models.CASCADE)
    batch = models.ForeignKey(Batch, blank = True, null = True, related_name = "enrollments", on_delete = models.CASCADE)
    roll_number = models.CharField(max_length = 25)
    joining_key = models.CharField(max_length = 8, null=True, blank=True, unique=True)
    student = models.ForeignKey("Student", related_name = "enrollment", null = True, on_delete = models.SET_NULL)
    date_joined = models.DateField(null = True)

    class Meta:
        unique_together = ('batch', 'roll_number')

    def __str__(self):
        if self.roll_number:
            return self.roll_number
        elif self.student:
            return self.student.user.name
        else:
            return self.pk

    def save(self, *args, **kwargs):
        errors = {}
        if self.batch not in self.institute.batches.all():
            errors['batch'] = ("This batch does not belong to the institute.",)
            raise ValidationError(errors)
        else:
            super(Enrollment, self).save(*args, **kwargs)

def pre_save_create_joining_key(sender, instance, *args, **kwargs):
    if not instance.joining_key:
        instance.joining_key= unique_random_key(instance)

pre_save.connect(pre_save_create_joining_key, sender=Enrollment)


class Student(models.Model):
    GENDERS = (("M", "Male"), ("F", "Female"), ("O", "Others"))
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    gender = models.CharField(max_length = 1, choices = GENDERS,blank=True,null=True)
    institutes = models.ManyToManyField(Institute, related_name = "students", through = Enrollment, blank = True)
    birth_date = models.DateField(null = True,blank=True)

    def __str__(self):
        return self.user.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.user.is_student = True
        super(Student, self).save(*args, **kwargs)

