# Generated by Django 3.0.3 on 2020-05-06 13:21

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0031_institute_links'),
    ]

    operations = [
        migrations.AddField(
            model_name='institute',
            name='forms',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=list, null=True),
        ),
    ]
