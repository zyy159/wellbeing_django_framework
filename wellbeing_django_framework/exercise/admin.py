from django.contrib import admin
from .models import Motion, Practice, Workout, Plan

# Register your models here.
class MotionAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "description", "created", "demo", "ready")
    list_filter = ("type","ready")


class WorkoutAdmin(admin.ModelAdmin):
    list_display = ("owner", "start_time", "end_time", "label", "score", "calories")
    list_filter = ("owner","label")


class PracticeAdmin(admin.ModelAdmin):
    list_display = ("workout", "start_time", "end_time", "owner", "motion", "score", "calories")
    list_filter = ("owner", "motion")


class PlanAdmin(admin.ModelAdmin):
    list_display = ("owner", "name", "motions", "schedule", "status")
    list_filter = ("owner", "status")


admin.site.register(Motion, MotionAdmin)
admin.site.register(Workout, WorkoutAdmin)
admin.site.register(Practice, PracticeAdmin)
admin.site.register(Plan, PlanAdmin)

