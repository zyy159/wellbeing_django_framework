# Generated by Django 3.2.18 on 2023-03-24 10:10

from django.db import migrations, models
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wellbeing_django_framework', '0010_alter_snippet_style'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snippet',
            name='highlighted',
            field=django_cryptography.fields.encrypt(models.TextField()),
        ),
    ]
