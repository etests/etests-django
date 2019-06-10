from django.db import models, migrations
from django.utils.text import slugify
from django.contrib.postgres.fields import ArrayField, JSONField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from datetime import datetime, timedelta
from authentication.models import User, Student, Institute
import random
import string
from .utils import get_unique_slug



def generateRandomKey(length = 10):
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(length))

class Exam(models.Model):
    id = models.AutoField(primary_key=True)
    position = models.IntegerField("position")
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=False, editable=False)
    image = models.ImageField(upload_to='static/images/exams/', default='static/images/exams/exam.png', max_length=20*1024, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, "name")
        super(Exam, self).save(*args, **kwargs)

    class Meta:
        ordering = ["position"]

    def __str__(self):
        return self.name

class Subject(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 100)
    slug = models.SlugField(unique = True, editable = False)
    image = models.ImageField(upload_to = 'static/images/subjects/', default = 'static/images/subjects/subject.png', max_length = 20*1024, blank = True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, "name")
        super(Subject, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Topic(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 100, blank = True)
    subject = models.ForeignKey(Subject, related_name = 'topics', blank = True, null = True, on_delete = models.CASCADE)
    image = models.ImageField(upload_to = 'static/images/topics/', default = 'static/images/topics/topic.png', max_length = 20*1024, blank = True)
    slug = models.SlugField(unique = True, editable = False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, "name")
        super(Topic, self).save(*args, **kwargs)

    class Meta:
        ordering = ["subject", "name"]

    def __str__(self):
        return self.name


class AccessCode(models.Model):
    id = models.AutoField(primary_key = True)
    limit = models.IntegerField()
    key = models.CharField(default = generateRandomKey, max_length = 10, unique=True)
    use_count = models.IntegerField(default = 0)

class Tag(models.Model):
    id = models.AutoField(primary_key = True)
    TAG_TYPE_CHOICES = (("EXAM", "Exam"), ("TOPIC", "Topic"), ("OTHER", "Others"))
    name = models.CharField(max_length = 20)
    type = models.CharField(max_length = 10, choices = TAG_TYPE_CHOICES)


class TestSeries(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 20)
    price = models.IntegerField()
    date_added = models.DateField(auto_now_add = True)
    slug = models.SlugField(unique = True, editable = False)
    visible = models.BooleanField(default = False)
    exam = models.ForeignKey(Exam, related_name = 'test_series', blank = True, null = True, on_delete = models.SET_NULL)
    institute = models.ForeignKey(Institute, related_name = 'test_series', blank = True, null = True, on_delete = models.CASCADE)
    registered_student = models.ManyToManyField(Student, related_name = 'test_series', blank = True)
    access_code = models.ForeignKey(AccessCode, related_name = 'test_series', blank = True, null = True, on_delete = models.SET_NULL)
    tags = models.ManyToManyField(Tag, related_name = 'test_series', blank = True)

    class Meta:
        verbose_name = 'Test Series'
        verbose_name_plural = 'Test Series'

    def __str__(self):
       return self.name

    def free(self):
        return self.price == 0

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, "name")
        super(TestSeries, self).save(*args, **kwargs)


QUESTION_TYPES = [
    ('SINGLE', 'SINGLE CORRECT'),
    ('MULTIPLE', 'MULTIPLE CORRECT'),
    ('NUMBER', 'NUMBER TYPE'),
    ('MATRIX', 'MATRIX MATCH')
]

class BaseTest(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 20)
    institute = models.ForeignKey(Institute, blank = True, null = True, on_delete = models.CASCADE)
    slug = models.SlugField(unique = True, editable = False)
    active = models.BooleanField(default = False)
    practice = models.BooleanField(default = False)
    tags = models.ManyToManyField(Tag, blank = True)
    date_added = models.DateField(auto_now_add = True)
    activation_time = models.DateField(blank = True, null = True)
    time_alotted = models.DurationField(default = timedelta(hours = 3))
    questions = JSONField()

    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, "name")
        super(BaseTest, self).save(*args, **kwargs)

class Test(BaseTest):
    id = models.AutoField(primary_key = True)
    test_series = models.ForeignKey(TestSeries, related_name = 'tests', blank = True, null = True, on_delete = models.CASCADE)

class UnitTest(BaseTest):
    id = models.AutoField(primary_key = True)
    visible = models.BooleanField(default = False)
    exam = models.ForeignKey(Exam, related_name = 'unit_tests', blank = True, null = True, on_delete = models.SET_NULL)
    registered_students = models.ManyToManyField(Student, blank = True)
    access_code = models.ForeignKey(AccessCode, related_name = 'unit_tests', blank = True, null = True, on_delete = models.SET_NULL)
    price = models.FloatField()

class Session(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name='sessions', on_delete=models.CASCADE)
    test = models.ForeignKey(Test, related_name='sessions', null=True, on_delete=models.CASCADE)
    practice = models.BooleanField(default = False)
    current = models.IntegerField(default=1)
    checkin_time = models.DateTimeField(auto_now_add = True)
    duration = models.DurationField(default = timedelta(hours = 3))
    response = JSONField()
    result = JSONField()

    def expired(self):
        if self.practice:
            return self.duration <= timedelta(seconds=0) or self.status==3
        else:
            return self.test.start_time+self.test.time_alotted<=timezone.now()
        
    def save(self, *args, **kwargs):
        if not self.practice:
            self.practice = self.test.practice

        super(Session, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ["-practice","user","test"]

class Buyer(models.Model):
    id = models.AutoField(primary_key=True)
    transaction_id = models.CharField(max_length=200)
    date_added = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="buyers", blank=True, null=True, on_delete=models.SET_NULL)
    amount=models.IntegerField(default=0)
    verified = models.BooleanField(default=False)
    content_type = models.ForeignKey(ContentType, blank = True, null = True, on_delete = models.SET_NULL)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.user.name