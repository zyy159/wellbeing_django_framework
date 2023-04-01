# Generated by Django 3.2.18 on 2023-04-01 01:36

import datetime
from django.db import migrations, models
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        ('exercise', '0003_auto_20230401_0911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='practice',
            name='calories',
            field=django_cryptography.fields.encrypt(models.IntegerField(default=0)),
        ),
        migrations.AlterField(
            model_name='practice',
            name='end_time',
            field=django_cryptography.fields.encrypt(models.DateTimeField(default=datetime.datetime(2023, 4, 1, 9, 36, 22, 994540))),
        ),
        migrations.AlterField(
            model_name='practice',
            name='score',
            field=django_cryptography.fields.encrypt(models.IntegerField(default=0)),
        ),
        migrations.AlterField(
            model_name='workout',
            name='calories',
            field=django_cryptography.fields.encrypt(models.IntegerField(default=0)),
        ),
        migrations.AlterField(
            model_name='workout',
            name='score',
            field=django_cryptography.fields.encrypt(models.IntegerField(default=0)),
        ),
    ]