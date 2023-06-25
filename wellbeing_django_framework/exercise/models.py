from django.db import models
from django_cryptography.fields import encrypt
from django.contrib.auth.models import User
from datetime import datetime
DJANGO_ENCRYPTED_FIELD_KEY = 'i3t_5lvb3KsDBPdAFdREdU7tinxCw7XVcwxg4YBmbKI='
DJANGO_ENCRYPTED_FIELD_ALGORITHM = 'AGCM'


class Wellbeing_user(models.Model):
    user_name = encrypt(models.CharField(max_length=100, blank=True, default=''))
    user_email = encrypt(models.CharField(max_length=100, blank=True, default=''))
    user_password = encrypt(models.CharField(max_length=100, blank=True, default=''))
    user_phone = encrypt(models.CharField(max_length=100, blank=True, default=''))
    create_time = encrypt(models.DateTimeField(auto_now_add=True))
    update_time = encrypt(models.DateTimeField(auto_now=True))
    user_status = encrypt(models.CharField(max_length=100, blank=True, default=''))
    user_type = encrypt(models.CharField(max_length=100, blank=True, default=''))
    last_login = encrypt(models.DateTimeField(auto_now_add=False))
    user_group = encrypt(models.CharField(max_length=100, blank=True, default=''))

    class Meta:
        ordering = ['-id']
        unique_together = ('user_name', 'user_email')
        # db_table = 'Wellbeing_user'
    def __str__(self):
        return self.user_name
class Exercise(models.Model):
    name = encrypt(models.CharField(max_length=100))
    popularity = models.IntegerField(default=0)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    score = models.IntegerField(default=0)
    calories = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Action(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    name = encrypt(models.CharField(max_length=100))
    popularity = models.IntegerField(default=0)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    image_url = encrypt(models.URLField())
    score = models.IntegerField(default=0)
    calories = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Model_store(models.Model):
    name = encrypt(models.CharField(max_length=100, blank=True, default=''))
    exercise = encrypt(models.CharField(max_length=100, blank=True, default=''))
    model_url = encrypt(models.TextField(default=''))
    created = encrypt(models.DateTimeField(auto_now_add=True))
    updated = encrypt(models.DateTimeField(auto_now=True))
    version = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name

class Schedule(models.Model):
    name = encrypt(models.CharField(max_length=100, blank=True, default=''))
    user = models.ForeignKey(Wellbeing_user, on_delete=models.CASCADE)
    date = models.DateField()
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    content = encrypt(models.CharField(max_length=500))
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    recurring_dates = encrypt(models.TextField(blank=True, null=True))


    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.exercise.name}"

# Create your models here.
# class Motion(models.Model):
#     motion_name = encrypt(models.CharField(max_length=100, blank=True, default=''))
#     motion_type = encrypt(models.CharField(max_length=100, blank=True, default=''))
#     motion_description = encrypt(models.TextField(default=''))
#     motion_created = encrypt(models.DateTimeField(auto_now_add=True))
#     motion_model_url = encrypt(models.TextField(default=''))
#     motion_start = encrypt(models.DateTimeField(auto_now_add=True))
#     motion_end = encrypt(models.DateTimeField(auto_now=True))
#     motion_version = models.IntegerField(default=0)
#     motion_demo = encrypt(models.TextField(default=''))
#     motion_ready = encrypt(models.BooleanField(default=False))
#     motion_popularity = models.IntegerField(default=0)
#     motion_model_type = encrypt(models.TextField(default=''))
#
#     class Meta:
#         ordering = ['-motion_created']
#
#     def __str__(self):
#         return self.type + ' - ' + self.name
#
# #demised

#
# #create the plan
# class Plan(models.Model):
#     plan_name = encrypt(models.CharField(max_length=100, blank=True, default=''))
#     plan_start = encrypt(models.DateTimeField(auto_now_add=True))
#     plan_end = encrypt(models.DateTimeField(auto_now=True))
#     plan_event = encrypt(models.JSONField(default=dict))
#     class Meta:
#         ordering = ['-id']
#
#     def __str__(self):
#         return self.type + ' - ' + self.name
#
# class Event(models.Model):
#     event_status_choice = [('not_start', 'Not Start'), ('cancel', 'Canceled'),('on_going', 'On Going'), ('completed', 'Completed'), ('expired', 'Expired')]
#     user = encrypt(models.JSONField(default=dict))
#     event_name = encrypt(models.CharField(max_length=100, blank=True, default=''))
#     motion_description = encrypt(models.TextField())
#     event_motions = encrypt(models.JSONField(default=dict))
#     schedule = encrypt(models.TextField())
#     status = encrypt(models.CharField(choices=event_status_choice, default='Not Start', max_length=100))
#     created = encrypt(models.DateTimeField(auto_now_add=True))
#     updated = encrypt(models.DateTimeField(auto_now=True))
#     event_start_time = encrypt(models.DateTimeField(auto_now_add=False,))
#     event_end_time = encrypt(models.DateTimeField(auto_now_add=False))
#     event_location = encrypt(models.TextField())
#     event_version = models.IntegerField(default=0)
#
#     class Meta:
#         ordering = ['-id']
#
#     def __str__(self):
#         return self.owner.username + ' - ' + self.name
#
#
# class Workout(models.Model):
#     workout_status_choice = [('not_start', 'Not Start'), ('cancel', 'Canceled'), ('on_going', 'On Going'),
#                            ('completed', 'Completed'), ('expired', 'Expired')]
#     user = encrypt(models.JSONField(default=dict))
#     event = encrypt(models.JSONField(default=dict))
#     start_time = encrypt(models.DateTimeField(auto_now_add=True))
#     end_time = encrypt(models.DateTimeField(auto_now_add=False))
#     label = encrypt(models.TextField())
#     score = models.IntegerField(default=0)
#     calories = models.IntegerField(default=0)
#     status = encrypt(models.CharField(choices=workout_status_choice, default='Not Start', max_length=100))
#
#     class Meta:
#         ordering = ['-id']
#
#     def __str__(self):
#         return self.owner.username + ' - ' + self.start_time.strftime("%m/%d/%Y, %H:%M:%S")
#
#
# # class Verification(models.Model):
# #     user = encrypt(models.JSONField(default=dict))
# #     ver_url = encrypt(models.TextField())
# #     ver_status=encrypt(models.CharField(max_length=100, blank=True, default=''))
# #     expire_time = encrypt(models.DateTimeField(auto_now_add=False))
# #
# #     class Meta:
# #         ordering = ['-id']
# #     def __str__(self):
# #         return self.owner.username + ' - ' + self.start_time.strftime("%m/%d/%Y, %H:%M:%S")
#     # def save(self, *args, **kwargs):
#     #     self.motion.popularity = self.motion.popularity + 1
#     #     self.motion.save()
#     #     super().save(*args, **kwargs)



class Resource_store(models.Model):
    resource_name = encrypt(models.TextField())
    resource_url = encrypt(models.TextField())
    resource_type = encrypt(models.CharField(max_length=100, blank=True, default=''))
    expire_time = encrypt(models.DateTimeField(auto_now_add=False))
    create_time = encrypt(models.DateTimeField(auto_now_add=True))
    update_time = encrypt(models.DateTimeField(auto_now=True))
    resource_version = models.IntegerField(default=0)

    class Meta:
        ordering = ['-id']
    def __str__(self):
        return self.owner.username + ' - ' + self.start_time.strftime("%m/%d/%Y, %H:%M:%S")
