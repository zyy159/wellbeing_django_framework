# Generated by Django 3.2.18 on 2023-03-30 13:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_cryptography.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Motion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', django_cryptography.fields.encrypt(models.CharField(blank=True, default='', max_length=100))),
                ('type', django_cryptography.fields.encrypt(models.CharField(blank=True, default='', max_length=100))),
                ('description', django_cryptography.fields.encrypt(models.TextField())),
                ('created', django_cryptography.fields.encrypt(models.DateTimeField(auto_now_add=True))),
                ('demo', django_cryptography.fields.encrypt(models.TextField())),
                ('ready', django_cryptography.fields.encrypt(models.BooleanField(default=False))),
            ],
        ),
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', django_cryptography.fields.encrypt(models.DateTimeField(auto_now_add=True))),
                ('end_time', django_cryptography.fields.encrypt(models.DateTimeField())),
                ('label', django_cryptography.fields.encrypt(models.TextField())),
                ('score', django_cryptography.fields.encrypt(models.IntegerField())),
                ('calories', django_cryptography.fields.encrypt(models.IntegerField())),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Practice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workout_label', django_cryptography.fields.encrypt(models.TextField())),
                ('start_time', django_cryptography.fields.encrypt(models.DateTimeField(auto_now_add=True))),
                ('end_time', django_cryptography.fields.encrypt(models.DateTimeField())),
                ('score', django_cryptography.fields.encrypt(models.IntegerField())),
                ('calories', django_cryptography.fields.encrypt(models.IntegerField())),
                ('motion', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='exercise.motion')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', django_cryptography.fields.encrypt(models.CharField(blank=True, default='', max_length=100))),
                ('motions', django_cryptography.fields.encrypt(models.JSONField())),
                ('schedule', django_cryptography.fields.encrypt(models.TextField())),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]