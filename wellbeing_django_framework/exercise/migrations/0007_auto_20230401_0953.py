# Generated by Django 3.2.18 on 2023-04-01 01:53

import datetime
from django.db import migrations, models
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        ('exercise', '0006_auto_20230401_0951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='practice',
            name='end_time',
            field=django_cryptography.fields.encrypt(models.DateTimeField(default=datetime.datetime(2023, 4, 1, 9, 53, 53, 913454))),
        ),
        migrations.AlterField(
            model_name='workout',
            name='end_time',
            field=django_cryptography.fields.encrypt(models.DateTimeField(default=datetime.datetime(2023, 4, 1, 9, 53, 53, 913454))),
        ),
    ]