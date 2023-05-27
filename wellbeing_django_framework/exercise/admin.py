from django.contrib import admin
from .models import *

# Register your models here.
class MotionAdmin(admin.ModelAdmin):
    list_display = ("motion_name", "motion_type", "motion_description", "motion_created", "motion_demo",
                    "motion_ready", "motion_popularity", "motion_model_type", "motion_model")
    list_filter = ("motion_type", "motion_ready")


class WorkoutAdmin(admin.ModelAdmin):
    list_display = ("user", "event", "start_time", "end_time", "label", "score", "calories", "status")
    list_filter = ("user", "label")


class Model_storeAdmin(admin.ModelAdmin):
    list_display = ("model_name", "model_type", "model_store_url", "created", "updated", "model_version")
    list_filter = ("model_name", "model_type")

class EventAdmin(admin.ModelAdmin):
    list_display = (
    "user", "event_name", "motion_description", "event_motions", "schedule", "status", "created", "updated",
    "event_start_time", "event_end_time", "event_location", "event_version")
    list_filter = ("user", "event_start_time", "event_end_time")

class VerificationAdmin(admin.ModelAdmin):
    list_display = ("user", "ver_url", "ver_status","expire_time")
    list_filter = ("user",)

class Wellbeing_userAdmin(admin.ModelAdmin):
    list_display = (
    "user_name", "user_email", "user_password", "user_phone", "create_time", "update_time", "user_status", "user_type",
    "last_login", "user_group")
    list_filter = ("user_name", "user_email")

class Resource_storeAdmin(admin.ModelAdmin):
        list_display = ("resource_name", "resource_url", "resource_type", "expire_time","create_time","update_time","resource_version")
        list_filter = ("resource_name",)


admin.site.register(Motion, MotionAdmin)
admin.site.register(Model_store, Model_storeAdmin)
admin.site.register(Workout, WorkoutAdmin)

admin.site.register(Event, EventAdmin)
admin.site.register(Verification, VerificationAdmin)
admin.site.register(Wellbeing_user, Wellbeing_userAdmin)
admin.site.register(Resource_store, Resource_storeAdmin)

