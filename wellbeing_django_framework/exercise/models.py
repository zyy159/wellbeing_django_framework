from django.db import models
from django_cryptography.fields import encrypt
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models.functions import TruncDate
from datetime import timedelta
from django.utils import timezone
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

class Model_store(models.Model):
    name = encrypt(models.CharField(max_length=100, blank=True, default=''))
    description = encrypt(models.TextField(default=''))
    duration = models.IntegerField(default=0)
    category = encrypt(models.CharField(max_length=100, blank=True, default=''))
    model_url = encrypt(models.TextField(default=''))
    created = encrypt(models.DateTimeField(auto_now_add=True))
    modified = encrypt(models.DateTimeField(auto_now=True))
    popularity = models.IntegerField(default=0)
    calories = models.IntegerField(default=0)
    version = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name


class Exercise(models.Model):
    name = encrypt(models.CharField(max_length=100))
    duration = models.IntegerField(default=0)
    popularity = models.IntegerField(default=0)
    category = encrypt(models.CharField(max_length=100, blank=True, default=''))
    model_stores = models.ManyToManyField(Model_store)

    def get_model_stores(self):
        models_names = [x.name for x in self.model_stores.all()]
        return models_names

    def __str__(self):
        return self.name


class Schedule(models.Model):
    owner = models.ForeignKey('auth.User', related_name='schedules', on_delete=models.CASCADE)
    name = encrypt(models.CharField(max_length=100, blank=True, default=''))
    exercises = models.ManyToManyField(Exercise)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    sub_schedules = encrypt(models.TextField())
    location = encrypt(models.TextField(default='front end url'))

    def get_exercises(self):
        exercises_names = [x.name for x in self.exercises.all()]
        return exercises_names

    def __str__(self):
        return f"{self.owner.__str__()} - {self.start_time} - {self.exercises}"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        # exercises = self.exercises.all()
        # for exercise in exercises:
        #     exercise.popularity = exercise.popularity + 1
        #     exercise.save()


class Action(models.Model):
    owner = models.ForeignKey('auth.User', related_name='actions', on_delete=models.CASCADE)
    model_store = models.ForeignKey(Model_store, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    score = models.IntegerField(default=0)
    calories = models.IntegerField(default=0)
    label = encrypt(models.TextField(blank=True))

    def __str__(self):
        return f"{self.owner.__str__()} - {self.start_time}"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        self.model_store.popularity = self.model_store.popularity + 1
        self.model_store.save()

        self.owner.profile.points += 2
        self.owner.profile.save()
        PointRecord.objects.create(owner=self.owner, points=2, remark=f'finished exercise {self.model_store.name}.')
        # 如果连续7天有记录，则多加50分
        if self.is_seven_days_active():
            self.owner.profile.points += 50
            self.owner.profile.save()
            PointRecord.objects.create(owner=self.owner, points=50, remark=f'Active for 7 consecutive days.')
        # 如果分数达到预定的各等级的分数，则获得该等级
        badges = Badge.objects.all().order_by('points')
        for badge in badges:
            if self.owner.profile.points >= badge.points and self.owner.profile.badge.points < badge.points:
                self.owner.profile.badge = badge
                self.owner.profile.save()
                UserBadge.objects.create(owner=self.owner, badge=badge, badge_points=badge.points)

        self.owner.usersummary.total_score = self.owner.usersummary.total_score + self.score
        self.owner.usersummary.total_calories = self.owner.usersummary.total_calories + self.calories
        self.owner.usersummary.total_time = self.owner.usersummary.total_time + sum([self.end_time - self.start_time], timedelta()).total_seconds()
        self.owner.usersummary.save()

    def is_seven_days_active(self):
        # 获取当前时间的前7天日期
        seven_days_ago = timezone.now() - timedelta(days=7)

        # 查询用户在过去7天内， 是否已经达成连续七天活跃
        pointRecords = PointRecord.objects.filter(owner=self.owner, points_date__gte=seven_days_ago)
        # 在 Python 中过滤 remark 字段
        pointRecords = [record for record in pointRecords if 'Active for 7 consecutive days.' in record.remark]
        # 已经达成连续七天活跃，则直接返回
        if len(pointRecords) != 0:
            return False

        # 查询用户在过去7天内的活动记录
        actions = Action.objects.filter(owner=self.owner, start_time__gte=seven_days_ago)

        # 将start_time字段截断为日期，并对每个日期进行计数
        actions_by_day = actions.annotate(day=TruncDate('start_time')).values('day').annotate(count=Count('id'))

        # 如果过去7天内每天都有记录，那么actions_by_day的长度应该是7
        return len(actions_by_day) == 7



class UserSummary(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    total_score = models.IntegerField(default=0)
    total_calories = models.IntegerField(default=0)
    total_time = models.IntegerField(default=0)
    current_month_score = models.IntegerField(default=0)
    current_month_calories = models.IntegerField(default=0)
    current_month_time = models.IntegerField(default=0)

# 定义用户可以兑换的奖励
class Reward(models.Model):
    name = encrypt(models.CharField(max_length=100, blank=True, default=''))
    description = encrypt(models.TextField(default=''))
    image_url = encrypt(models.TextField(default=''))
    points = models.IntegerField(default=0)

# 定义用户可以获得的徽章
class Badge(models.Model):
    name = encrypt(models.CharField(max_length=100, blank=True, default=''))
    description = encrypt(models.TextField(default=''))
    image_url = encrypt(models.TextField(default=''))
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    @classmethod
    def get_default(cls):
        return cls.objects.order_by('points').first()



# 用户兑换奖励的记录
class UserReward(models.Model):
    owner = models.ForeignKey('auth.User', related_name='userrewards', on_delete=models.CASCADE)
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE)
    reward_points = models.IntegerField(default=0)
    reward_date = models.DateTimeField(auto_now_add=True)



# 用户获得的徽章记录
class UserBadge(models.Model):
    owner = models.ForeignKey('auth.User', related_name='userbadges', on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    badge_points = models.IntegerField(default=0)
    badge_date = models.DateTimeField(auto_now_add=True)


# 用户拥有的积分
class PointRecord(models.Model):
    owner = models.ForeignKey('auth.User', related_name='pointrecord', on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    remark = encrypt(models.TextField(default=''))
    points_date = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    used_points = models.IntegerField(default=0)
    badge = models.ForeignKey(Badge, on_delete=models.SET_NULL, null=True, default=Badge.get_default)


class Like(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_given')
    likee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_received')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('liker', 'likee')

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
