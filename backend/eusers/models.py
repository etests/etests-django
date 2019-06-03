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
from django.utils.text import slugify
import random
import string


def randomStringDigits(stringLength=20):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))


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
    name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, blank=True, null=True, unique=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user is a staff member."),
    )
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    phone = models.CharField(max_length=15, blank=False, null=False, unique=True)
    state = models.CharField(max_length=100, blank=False)
    city = models.CharField(max_length=100, blank=False)
    date_joined = models.DateField(auto_now_add=True)
    is_student = models.BooleanField(default=False)
    is_institute = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    objects = MyUserManager()

    def __str__(self):
        return self.name


@receiver(pre_save, sender=User)
def set_username(sender, instance, **kwargs):
    if not instance.username:
        username = "_".join(instance.name.split()).lower()
        counter = 1
        if User.objects.filter(username=username):
            next_username = instance.email.split("@")[0]
        else:
            next_username = username
        while User.objects.filter(username=next_username):
            next_username = username + str(counter)
            counter += 1
        instance.username = next_username


models.signals.pre_save.connect(set_username, sender=User)


class Institute(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pincode = models.CharField(max_length=20, blank=False)

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
    birth_date = models.DateField(blank=False, null=False)

    def __str__(self):
        return self.user.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.user.is_student = True
        super(Student, self).save(*args, **kwargs)

class Exam(models.Model):
    id = models.AutoField(primary_key=True)
    position = models.IntegerField("position")
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=False, editable=False)
    image = models.ImageField(upload_to='static/images/exams/', default='static/images/exams/exam.png', max_length=20*1024, blank=True)
    link = models.CharField(max_length=500)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Exam, self).save(*args, **kwargs)

    class Meta:
        ordering = ["position"]

    def __str__(self):
        return self.name

class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=False, editable=False)
    image = models.ImageField(upload_to='static/images/subjects/', default='static/images/subjects/subject.png', max_length=20*1024, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Subject, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Topic(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True)
    subject = models.ForeignKey(Subject, related_name='topics', blank=True, null=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='static/images/topics/', default='static/images/topics/topic.png', max_length=20*1024, blank=True)
    slug = models.SlugField(unique=False, editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Topic, self).save(*args, **kwargs)

    class Meta:
        ordering = ["subject", "name"]

    def __str__(self):
        return self.name


class AccessCode(models.Model):
    id = models.AutoField(primary_key=True)
    limit = models.IntegerField(blank=False)
    key = models.CharField(max_length=20, blank=True)
    use_count = models.IntegerField(blank=True,null=True)

    def save(self, *args, **kwargs):
        self.key = randomStringDigits()
        super(AccessCode, self).save(*args, **kwargs)

class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    label = (("E", "Exam_Related"), ("S", "Subject_Related"), ("O", "Others"))
    name = models.CharField(max_length=20, blank=False)
    type = models.CharField(max_length=1, choices=label)


class TestSeries(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, blank=False)
    price = models.IntegerField(blank=False)
    date_added = models.DateField(auto_now_add=True)
    slug = models.SlugField(unique=False, editable=False)
    visible = models.BooleanField(default=False)
    practice = models.BooleanField(default=False)
    exam = models.ForeignKey(Exam, related_name='testseries', blank=True, null=True, on_delete=models.CASCADE)
    institute = models.ForeignKey(Institute, related_name='testseries', blank=True, null=True, on_delete=models.CASCADE)
    registered_student = models.ManyToManyField(Student, related_name='testseries', blank=True)
    access_code = models.ForeignKey(AccessCode, related_name='testseries', blank=True, null=True, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='testseries', blank=True)

    class Meta:
        verbose_name = 'Test Series'
        verbose_name_plural = 'Test Series'
    def __str__(self):
       return self.name
    def free(self):
        return self.price==0


class BaseTest(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, blank=False)
    slug = models.SlugField(unique=False, editable=False)
    active = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, blank=True)
    duration = models.DurationField(default=timedelta(hours=3),null=False)
    start_time = models.DateField(blank=True, null=True)

    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Topic, self).save(*args, **kwargs)

class Test(BaseTest):
    id = models.AutoField(primary_key=True)
    test_series = models.ForeignKey(TestSeries, related_name='tests', blank=True, null=True, on_delete=models.CASCADE)

class UnitTest(BaseTest):
    id = models.AutoField(primary_key=True)
    visible = models.BooleanField(default=False)
    practice = models.BooleanField(default=False)
    exam = models.ForeignKey(Exam, related_name='unit_tests', blank=True, null=True, on_delete=models.CASCADE)
    institute = models.ForeignKey(Institute, related_name='unit_tests', blank=True, null=True, on_delete=models.CASCADE)
    registered_student = models.ManyToManyField(Student, related_name='unit_tests', blank=True)
    access_code = models.ForeignKey(AccessCode, related_name='unit_tests', blank=True, null=True, on_delete=models.CASCADE)
    price = models.IntegerField(blank=False)