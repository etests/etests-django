# Generated by Django 3.0.3 on 2020-05-29 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0033_user_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='site',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
