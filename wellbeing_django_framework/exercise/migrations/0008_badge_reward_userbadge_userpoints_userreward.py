# Generated by Django 3.2.18 on 2023-08-19 08:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exercise', '0007_model_store_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', django_cryptography.fields.encrypt(models.CharField(blank=True, default='', max_length=100))),
                ('description', django_cryptography.fields.encrypt(models.TextField(default=''))),
                ('image', django_cryptography.fields.encrypt(models.ImageField(default='', upload_to='badge_images'))),
                ('points', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', django_cryptography.fields.encrypt(models.CharField(blank=True, default='', max_length=100))),
                ('description', django_cryptography.fields.encrypt(models.TextField(default=''))),
                ('image', django_cryptography.fields.encrypt(models.ImageField(default='', upload_to='reward_images'))),
                ('points', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='UserReward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reward_points', models.IntegerField(default=0)),
                ('reward_date', models.DateTimeField(auto_now_add=True)),
                ('reward', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exercise.reward')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserPoints',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField(default=0)),
                ('remark', django_cryptography.fields.encrypt(models.TextField(default=''))),
                ('points_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserBadge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('badge_points', models.IntegerField(default=0)),
                ('badge_date', models.DateTimeField(auto_now_add=True)),
                ('badge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exercise.badge')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
