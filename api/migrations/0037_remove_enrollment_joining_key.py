# Generated by Django 3.0.3 on 2020-06-27 05:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0036_auto_20200627_1030'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enrollment',
            name='joining_key',
        ),
    ]
