# Generated by Django 3.0.3 on 2020-03-18 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20200305_1534'),
    ]

    operations = [
        migrations.AddField(
            model_name='institute',
            name='joined_students',
            field=models.ManyToManyField(related_name='joined_institutes', to='api.Student'),
        ),
    ]