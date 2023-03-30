from django.contrib import admin
from .models import Motion, Practice, Workout, Plan

# Register your models here.
class MotionAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "description", "created", "demo", "ready")
    list_filter = ("type","ready")


admin.site.register(Motion, MotionAdmin)
