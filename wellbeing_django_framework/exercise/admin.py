from django.contrib import admin
from .models import *

# Register your models here.
# class MotionAdmin(admin.ModelAdmin):
#     list_display = ("motion_name", "motion_type", "motion_description", "motion_created", "motion_model_url",
#                     "motion_start","motion_end","motion_version",
#                     "motion_demo",
#                     "motion_ready", "motion_popularity", "motion_model_type")
#     list_filter = ("motion_type", "motion_ready")
#
#
# class WorkoutAdmin(admin.ModelAdmin):
#     list_display = ("user", "event", "start_time", "end_time", "label", "score", "calories", "status")
#     list_filter = ("user", "label")
#
# # class Model_storeAdmin(admin.ModelAdmin):
# #     list_display = ("model_name", "model_type", "model_store_url", "created", "updated", "model_version")
# #     list_filter = ("model_name", "model_type")
#
# class EventAdmin(admin.ModelAdmin):
#     list_display = (
#     "user", "event_name", "motion_description", "event_motions", "schedule", "status", "created", "updated",
#     "event_start_time", "event_end_time", "event_location", "event_version")
#     list_filter = ("user", "event_start_time", "event_end_time")
#
#
# # class VerificationAdmin(admin.ModelAdmin):
# #     list_display = ("user", "ver_url", "ver_status","expire_time")
# #     list_filter = ("user",)

class Wellbeing_userAdmin(admin.ModelAdmin):
    list_display = (
    "user_name", "user_email", "user_password", "user_phone", "create_time", "update_time", "user_status", "user_type",
    "last_login", "user_group")
    list_filter = ("user_name", "user_email")

class Resource_storeAdmin(admin.ModelAdmin):
        list_display = ("resource_name", "resource_url", "resource_type", "expire_time","create_time","update_time",
                        "resource_version")
        list_filter = ("resource_name",)


class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("name", "duration", "popularity", "category", "get_model_stores")
    raw_id_fields = ("model_stores",)
    list_filter = ("name",)
    search_fields = ['foreign_key__related_fieldname']

class ActionAdmin(admin.ModelAdmin):
    list_display = ("owner","model_store", "start_time", "end_time", "score", "calories", "label")
    list_filter = ("owner", "model_store")

class Model_storeAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "duration", "category", "model_url", "created", "modified", "popularity", "calories", "version")
    list_filter = ("name",)


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("owner", "name", "get_exercises", "start_time", "end_time", "sub_schedules")
    raw_id_fields = ("exercises",)
    list_filter = ("owner",)


class UserSummaryAdmin(admin.ModelAdmin):
    list_display = ("owner", "total_score", "total_calories", "total_time", "current_month_score",
                    "current_month_calories", "current_month_time")
    list_filter = ("owner",)


class RewardAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "image_url", "points")
    list_filter = ("name",)


class BadgeAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "image_url", "points")
    list_filter = ("name",)


class UserRewardAdmin(admin.ModelAdmin):
    list_display = ("owner", "reward", "reward_points", "reward_date")
    list_filter = ("owner",)


class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ("owner", "badge", "badge_points", "badge_date")
    list_filter = ("owner",)


class PointRecordAdmin(admin.ModelAdmin):
    list_display = ("owner", "points", "remark", "points_date")
    list_filter = ("owner",)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("owner", "points", "badge")
    list_filter = ("owner",)



admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Model_store, Model_storeAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Wellbeing_user, Wellbeing_userAdmin)
admin.site.register(Resource_store, Resource_storeAdmin)
admin.site.register(UserSummary, UserSummaryAdmin)
admin.site.register(Reward, RewardAdmin)
admin.site.register(Badge, BadgeAdmin)
admin.site.register(UserReward, UserRewardAdmin)
admin.site.register(UserBadge, UserBadgeAdmin)
admin.site.register(PointRecord, PointRecordAdmin)
admin.site.register(Profile, ProfileAdmin)