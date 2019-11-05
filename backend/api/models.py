from django.db import models, migrations
from django.utils.text import slugify
from django.contrib.postgres.fields import ArrayField, JSONField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from django.utils import timezone
from authentication.models import User, Student, Institute
import random
import string
from .utils import get_unique_slug
from etests.storage_backends import *

def validate_file_size(file):

    if file.size > 153600:
        raise ValidationError("The maximum image size is 150 KB.")
    else:
        return file


def generateRandomKey(length=10):
    return "".join(
        random.choice(string.ascii_letters + string.digits) for i in range(length)
    )


class Exam(models.Model):
    id = models.AutoField(primary_key=True)
    position = models.IntegerField("position")
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=False, editable=False)
    image = models.CharField(
        default="exam.png", max_length=20 * 1024, blank=True, null=True
    )
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ["position"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, "name")
        super(Exam, self).save(*args, **kwargs)


class AccessCode(models.Model):
    id = models.AutoField(primary_key=True)
    limit = models.IntegerField()
    key = models.CharField(default=generateRandomKey, max_length=10, unique=True)
    use_count = models.IntegerField(default=0)

    def __str__(self):
        return self.key


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    TAG_TYPE_CHOICES = (("EXAM", "Exam"), ("TOPIC", "Topic"), ("OTHER", "Others"))
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=10, choices=TAG_TYPE_CHOICES)

    def __str__(self):
        return self.name

class Offer(models.Model):
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=1024)


class TestSeries(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    date_added = models.DateField(auto_now_add=True)
    slug = models.SlugField(unique=True, editable=False)
    visible = models.BooleanField(default=False)
    exams = models.ManyToManyField(Exam, related_name="test_series", blank=True)
    offers = models.ManyToManyField(Offer, related_name="test_series", blank=True)
    discount = models.IntegerField(default=0)
    institute = models.ForeignKey(
        Institute,
        related_name="test_series",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    registered_students = models.ManyToManyField(Student, blank=True)
    access_code = models.ForeignKey(
        AccessCode,
        related_name="test_series",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    tags = models.ManyToManyField(Tag, related_name="test_series", blank=True)
    tests = models.ManyToManyField("Test", related_name="test_series", blank=True)

    class Meta:
        verbose_name = "Test Series"
        verbose_name_plural = "Test Series"

    def __str__(self):
        return self.name

    def free(self):
        return self.price == 0

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, "name")
        super(TestSeries, self).save(*args, **kwargs)


class Test(models.Model):
    id = models.AutoField(primary_key=True)
    registered_students = models.ManyToManyField(Student, blank=True)
    name = models.CharField(max_length=200)
    institute = models.ForeignKey(
        Institute, blank=True, null=True, on_delete=models.CASCADE
    )
    slug = models.SlugField(unique=True, editable=False)
    exam = models.ForeignKey(
        Exam, related_name="tests", blank=True, null=True, on_delete=models.SET_NULL
    )
    aits = models.BooleanField(default=False)
    practice = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    activation_time = models.DateTimeField(blank=True, null=True)
    closing_time = models.DateTimeField(blank=True, null=True)
    time_alotted = models.DurationField(default=timedelta(hours=3))
    sections = JSONField(blank=True, null=True)
    questions = JSONField(blank=True, null=True)
    answers = JSONField(blank=True, null=True)
    stats = JSONField(blank=True, null=True)
    corrected = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    visible = models.BooleanField(default=True)
    free = models.BooleanField(default=False)
    marks_list = JSONField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, "name")
        super(Test, self).save(*args, **kwargs)

    @property
    def status(self):
        if not self.activation_time or timezone.now() < self.activation_time:
            return 0
        elif (
            not self.closing_time
            or self.activation_time <= timezone.now()
            and timezone.now() < self.closing_time
        ):
            return 1
        elif self.closing_time <= timezone.now():
            if not self.corrected and not self.finished:
                return 2
            elif not self.finished:
                return 3
            else:
                return 4

    def __str__(self):
        return self.name


class Session(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(
        Student, related_name="sessions", on_delete=models.CASCADE
    )
    test = models.ForeignKey(
        Test, related_name="sessions", null=True, on_delete=models.CASCADE
    )
    practice = models.BooleanField(default=False)
    checkin_time = models.DateTimeField(default=timezone.now)
    duration = models.DurationField(default=timedelta(hours=3))
    completed = models.BooleanField(default=False)
    response = JSONField(blank=True, null=True)
    result = JSONField(blank=True, null=True)
    current = JSONField(blank=True, null=True)
    marks = JSONField(blank=True, null=True)
    ranks = JSONField(blank=True, null=True)

    def __str__(self):
        return self.student.user.name + " " + self.test.name

    def expired(self):
        if self.practice:
            return self.duration <= timedelta(seconds=0) or self.status == 3
        else:
            return self.test.start_time + self.test.time_alotted <= timezone.now()

    class Meta:
        ordering = ["-practice", "student", "test"]


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    transaction_id = models.CharField(max_length=200)
    receipt = models.FileField(storage=PrivateMediaStorage(), null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)
    user = models.ForeignKey(
        User, related_name="payments", blank=True, null=True, on_delete=models.SET_NULL
    )
    amount = models.IntegerField(default=0)
    verified = models.BooleanField(default=False)
    test_series = models.ForeignKey(
        TestSeries, blank=True, null=True, on_delete=models.SET_NULL
    )
    show = models.BooleanField(default=False)

    def __str__(self):
        return self.user.name

    def save(self, *args, **kwargs):
        if self.verified:
            self.test_series.registered_students.add(self.user.student)
            for test in self.test_series.tests.all():
                test.registered_students.add(self.user.student)

        super(Payment, self).save(*args, **kwargs)


class Variable(models.Model):
    name = models.CharField(max_length=100)
    value = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    TRANSACTIONS_TYPE_CHOICES = (
        ("CASH", "Cash"),
        ("UPI", "UPI"),
        ("NETBANKING", "Netbanking"),
        ("PAYTM", "PayTM"),
        ("OTHERS", "Others"),
    )
    id = models.AutoField(primary_key=True)
    institute = models.ForeignKey(Institute, null=True, on_delete=models.SET_NULL)
    date_added = models.DateField(auto_now_add=True)
    credits_added = models.IntegerField(default=0)
    transaction_id = models.CharField(
        max_length=200, null=True, blank=True, unique=True
    )
    mode = models.CharField(max_length=10, choices=TRANSACTIONS_TYPE_CHOICES)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return (
            self.institute.user.name
            + "/Mode-"
            + self.mode
            + "/TID-"
            + self.transaction_id
        )

    def save(self, *args, **kwargs):
        if self.pk is None:
            try:
                self.credits_added = (
                    self.amount * Variable.objects.get(name="CREDITS_PER_RUPEE").value
                )
            except:
                self.credits_added = 0
            institute = self.institute
            institute.current_credits += self.credits_added
            institute.save()
        super().save(*args, **kwargs)


class CreditUse(models.Model):
    id = models.AutoField(primary_key=True)
    institute = models.ForeignKey(Institute, null=True, on_delete=models.SET_NULL)
    test = models.ForeignKey(Test, null=True, on_delete=models.SET_NULL)
    date_added = models.DateField(auto_now_add=True)
    credits_used = models.IntegerField(default=0)

    def __str__(self):
        return (
            self.institute.user.name
            + " / "
            + str(self.date_added)
            + " / "
            + str(self.credits_used)
        )

    def save(self, *args, **kwargs):
        if self.pk is None:
            institute = self.institute
            # Later: calculate credits_used using fixed rate
            institute.current_credits -= self.credits_used
            institute.save()
        super().save(*args, **kwargs)


class ResetCode(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, related_name="codes", blank=True, null=True, on_delete=models.SET_NULL
    )
    reset_code = models.CharField(max_length=6)
    date_added = models.DateField(auto_now_add=True)
    done = models.BooleanField(default=False)


class AITSTransaction(models.Model):
    TRANSACTIONS_TYPE_CHOICES = (
        ("CASH", "Cash"),
        ("UPI", "UPI"),
        ("NETBANKING", "Netbanking"),
        ("PAYTM", "PayTM"),
        ("OTHERS", "Others"),
    )
    id = models.AutoField(primary_key=True)
    institute = models.ForeignKey(Institute, null=True, on_delete=models.SET_NULL)
    date_added = models.DateField(auto_now_add=True)
    transaction_id = models.CharField(
        max_length=200, null=True, blank=True, unique=True
    )
    mode = models.CharField(max_length=10, choices=TRANSACTIONS_TYPE_CHOICES)
    amount = models.IntegerField(default=0)
    remarks = models.CharField(max_length=50, blank=True, null=True)
    test_series = models.ManyToManyField(
        TestSeries, related_name="aits_transactions", blank=False
    )
    receipt = models.FileField(storage=PrivateMediaStorage(), null=True)

    def __str__(self):
        return (
            self.institute.user.name
            + "/Mode-"
            + self.mode
            + "/TID-"
            + self.transaction_id
        )


class Question(models.Model):
    TYPES = (
        ("0", "Single Correct"),
        ("1", "Multiple Correct"),
        ("2", "Numerical"),
        ("3", "Matrix Match"),
    )
    LEVELS = (
        ("0", "Very Easy"),
        ("1", "Easy"),
        ("2", "Medium"),
        ("3", "Hard"),
        ("4", "Very Hard"),
    )
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=20000)
    answer = JSONField()
    solution = models.CharField(max_length=20000)
    type = models.CharField(max_length=10, choices=TYPES)
    subjectIndex = models.IntegerField()
    topicIndex = models.IntegerField()
    difficulty = models.CharField(max_length=10, choices=LEVELS)

class QuestionImage(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.ImageField(storage=PublicMediaStorage(), validators=[validate_file_size])
