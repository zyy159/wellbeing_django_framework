# Generated by Django 3.2.18 on 2023-03-24 10:08

from django.db import migrations, models
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wellbeing_django_framework', '0004_auto_20230321_2024'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='snippet',
            name='created',
        ),
        migrations.AddField(
            model_name='snippet',
            name='created',
            field=django_cryptography.fields.encrypt(models.DateTimeField(auto_now_add=True)),
        ),
    ]
