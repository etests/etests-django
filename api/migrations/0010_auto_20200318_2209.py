# Generated by Django 3.0.3 on 2020-03-18 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_institute_joined_students'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='enrollment',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='enrollment',
            name='batch',
        ),
        migrations.RemoveField(
            model_name='enrollment',
            name='institute',
        ),
        migrations.RemoveField(
            model_name='enrollment',
            name='student',
        ),
        migrations.RemoveField(
            model_name='institute',
            name='joined_students',
        ),
        migrations.RemoveField(
            model_name='student',
            name='institutes',
        ),
        migrations.RemoveField(
            model_name='test',
            name='registered_batches',
        ),
        migrations.AddField(
            model_name='institute',
            name='students',
            field=models.ManyToManyField(related_name='institutes', to='api.Student'),
        ),
        migrations.DeleteModel(
            name='Batch',
        ),
        migrations.DeleteModel(
            name='Enrollment',
        ),
    ]
