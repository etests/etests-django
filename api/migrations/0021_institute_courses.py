# Generated by Django 3.0.3 on 2020-04-08 15:19

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_contact_date_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='institute',
            name='courses',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=list),
        ),
    ]