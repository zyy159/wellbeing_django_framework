from django.db import models
from django_cryptography.fields import encrypt
from django.contrib.auth.models import User

# Create your models here.
class Motion(models.Model):
    name = encrypt(models.CharField(max_length=100, blank=True, default=''))
    type = encrypt(models.CharField(max_length=100, blank=True, default=''))
    description = encrypt(models.TextField())
    created = encrypt(models.DateTimeField(auto_now_add=True))
    demo = encrypt(models.TextField())
    ready = encrypt(models.BooleanField(default=False))

    def __str__(self):
        return self.type + ' - ' + self.name


class Practice(models.Model):
    workout_label = encrypt(models.TextField())
    start_time = encrypt(models.DateTimeField(auto_now_add=True))
    end_time = encrypt(models.DateTimeField(auto_now_add=False))
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    motion = models.ForeignKey(Motion, on_delete=models.RESTRICT)
    score = encrypt(models.IntegerField())
    calories = encrypt(models.IntegerField())


class Workout(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = encrypt(models.DateTimeField(auto_now_add=True))
    end_time = encrypt(models.DateTimeField(auto_now_add=False))
    label = encrypt(models.TextField())
    score = encrypt(models.IntegerField())
    calories = encrypt(models.IntegerField())


class Plan(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = encrypt(models.CharField(max_length=100, blank=True, default=''))
    motions = encrypt(models.JSONField())
    schedule = encrypt(models.TextField())
