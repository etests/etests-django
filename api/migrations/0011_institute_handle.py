# Generated by Django 3.0.3 on 2020-03-21 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20200318_2209'),
    ]

    operations = [
        migrations.AddField(
            model_name='institute',
            name='handle',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]