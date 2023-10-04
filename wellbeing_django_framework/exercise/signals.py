from django.utils import timezone

from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver

from wellbeing_django_framework.exercise.models import Profile, PointRecord, Badge, UserBadge


def add_points(sender, user, request, **kwargs):
    # 获取用户所有的积分记录
    point_records = PointRecord.objects.filter(owner=user).order_by('-points_date')

    # 找到最后一次登录获得积分的记录
    last_login_point_record = None
    for record in point_records:
        if record.remark == "Logged in":
            last_login_point_record = record
            break

    # 如果用户还没有因为登录获得过积分，或者最后一次因为登录获得积分不是在今天，那么给用户加5分
    if last_login_point_record is None or last_login_point_record.points_date.date() < timezone.now().date():
        user.profile.points += 5
        user.profile.save()
        PointRecord.objects.create(owner=user, points=5, remark="Logged in")
        # 检查用户是否达成某个等级
        badges = Badge.objects.all().order_by('points')
        for badge in badges:
            if user.profile.points >= badge.points and (user.profile.badge is None or user.profile.badge.points < badge.points):
                user.profile.badge = badge
                user.profile.save()
                UserBadge.objects.create(owner=user, badge=badge, badge_points=badge.points)

user_logged_in.connect(add_points)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(owner=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()