from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField

class Question(models.Model):
    section = models.IntegerField(default=0),
    text = models.CharField(max_length=2048),
    image = models.CharField(max_length=2048),
    type = models.IntegerField(default=0),
    options = ArrayField(models.CharField(max_length=1024), default = lambda _ : ("Option A", "Option B", "Option C", "Option D")),
    status = models.IntegerField(default=0),
    correctMarks = models.IntegerField(default=0),
    incorrectMarks = models.IntegerField(default=0),
    answers = ArrayField(models.CharField(max_length=1024), default = lambda _ : ("Answer P", "Answer Q", "Answer R", "Answer S", "Answer T"))