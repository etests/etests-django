# Generated by Django 2.2.1 on 2019-09-19 13:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_auto_20190919_1928'),
    ]

    operations = [
        migrations.RenameField(
            model_name='testseries',
            old_name='exam',
            new_name='exams',
        ),
    ]
