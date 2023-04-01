from django.db import models
from django_cryptography.fields import encrypt
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.
class Motion(models.Model):
    name = encrypt(models.CharField(max_length=100, blank=True, default=''))
    type = encrypt(models.CharField(max_length=100, blank=True, default=''))
    description = encrypt(models.TextField())
    created = encrypt(models.DateTimeField(auto_now_add=True))
    demo = encrypt(models.TextField())
    ready = encrypt(models.BooleanField(default=False))
    popularity = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.type + ' - ' + self.name



class Plan(models.Model):
    plan_status_choice = [('not_start', 'Not Start'), ('on_going', 'On Going'), ('completed', 'Completed'), ('expired', 'Expired')]
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = encrypt(models.CharField(max_length=100, blank=True, default=''))
    motions = encrypt(models.JSONField())
    schedule = encrypt(models.TextField())
    status = encrypt(models.CharField(choices=plan_status_choice, default='Not Start', max_length=100))

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.owner.username + ' - ' + self.name


class Workout(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, blank=True, null=True, on_delete=models.SET_NULL)
    start_time = encrypt(models.DateTimeField(auto_now_add=True))
    end_time = encrypt(models.DateTimeField(auto_now_add=False, default=datetime.now()))
    label = encrypt(models.TextField())
    score = encrypt(models.IntegerField(default=0))
    calories = encrypt(models.IntegerField(default=0))

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.owner.username + ' - ' + self.start_time.strftime("%m/%d/%Y, %H:%M:%S")


class Practice(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    start_time = encrypt(models.DateTimeField(auto_now_add=True))
    end_time = encrypt(models.DateTimeField(auto_now_add=False, default=datetime.now()))
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    motion = models.ForeignKey(Motion, on_delete=models.RESTRICT)
    score = encrypt(models.IntegerField(default=0))
    calories = encrypt(models.IntegerField(default=0))

    class Meta:
        ordering = ['-id']

    def save(self, *args, **kwargs):
        self.motion.popularity = self.motion.popularity + 1
        self.motion.save()
        super().save(*args, **kwargs)
