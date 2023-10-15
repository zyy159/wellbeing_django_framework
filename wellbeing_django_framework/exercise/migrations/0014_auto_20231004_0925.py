# Generated by Django 3.2.18 on 2023-10-04 01:25

from django.db import migrations, models
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        ('exercise', '0013_profile_badge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='badge',
            name='image',
        ),
        migrations.RemoveField(
            model_name='reward',
            name='image',
        ),
        migrations.AddField(
            model_name='badge',
            name='image_url',
            field=django_cryptography.fields.encrypt(models.TextField(default='')),
        ),
        migrations.AddField(
            model_name='reward',
            name='image_url',
            field=django_cryptography.fields.encrypt(models.TextField(default='')),
        ),
    ]