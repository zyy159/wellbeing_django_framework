# Generated by Django 3.2.18 on 2023-09-21 14:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exercise', '0010_auto_20230921_2219'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='user',
            new_name='owner',
        ),
    ]