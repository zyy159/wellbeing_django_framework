# Generated by Django 3.2.18 on 2023-07-02 13:07

from django.db import migrations, models
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        ('exercise', '0002_auto_20230701_1243'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='category',
            field=django_cryptography.fields.encrypt(models.CharField(blank=True, default='', max_length=100)),
        ),
        migrations.AddField(
            model_name='exercise',
            name='duration',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='exercise',
            name='popularity',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='model_store',
            name='calories',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='model_store',
            name='duration',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='action',
            name='label',
            field=django_cryptography.fields.encrypt(models.TextField(blank=True)),
        ),
    ]
