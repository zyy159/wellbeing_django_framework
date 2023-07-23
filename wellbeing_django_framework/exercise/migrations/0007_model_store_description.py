# Generated by Django 3.2.18 on 2023-07-02 14:11

from django.db import migrations, models
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        ('exercise', '0006_schedule_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='model_store',
            name='description',
            field=django_cryptography.fields.encrypt(models.TextField(default='')),
        ),
    ]