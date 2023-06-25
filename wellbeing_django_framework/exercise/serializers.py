from rest_framework import serializers
from .models import *



# class MotionSerializer(serializers.HyperlinkedModelSerializer):
#
#     class Meta:
#         model = Motion
#         fields = [ 'id', "motion_name", "motion_type", "motion_description", "motion_created", "motion_model_url","motion_start","motion_end",
#                    "motion_demo",   "motion_ready", "motion_popularity", "motion_model_type"]
#
# class WorkoutSerializer(serializers.HyperlinkedModelSerializer):
#     user = serializers.ReadOnlyField(source='owner.username')
#     class Meta:
#         model = Workout
#         fields = ['url', 'id', "user", "event", "start_time", "end_time", "label", "score", "calories", "status"]
#
#
# class EventSerializer(serializers.HyperlinkedModelSerializer):
#     user = serializers.ReadOnlyField(source='owner.username')
#     class Meta:
#         model = Event
#         fields = ['url', 'id',  "user", "event_name", "motion_description", "event_motions", "schedule", "status", "created", "updated",
#     "event_start_time", "event_end_time", "event_location", "event_version"]

# class Model_storeSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Model_store
#         fields = ['url', 'id', "model_name", "model_type", "model_store_url", "created", "updated", "model_version"]

# class VerificationSerializer(serializers.HyperlinkedModelSerializer):
#     user = serializers.ReadOnlyField(source='owner.username')
#     class Meta:
#         model = Verification
#         fields = ['url', 'id',  "user", "ver_url", "ver_status","expire_time"]

class Wellbeing_userSerializer(serializers.HyperlinkedModelSerializer):
    user_name = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Wellbeing_user
        fields = ['url', 'id',  "user_name", "user_email", "user_password", "user_phone", "create_time", "update_time", "user_status", "user_type",
    "last_login", "user_group"]

class Resource_storeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Resource_store
        fields = ['url', 'id',  "resource_name", "resource_url", "resource_type", "expire_time","create_time","update_time","resource_version"]

class ExerciseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Exercise
        fields = ['name', 'popularity',  "resource_name", "start_time", "end_time", "score","calories"]

class ActionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Action
        fields = ['exercise', 'name',  "popularity", "start_time", "end_time", "image_url","score","calories"]

class Model_storeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Model_store
        fields = ['name', 'exercise',  "model_url", "created", "updated", "version"]

class ScheduleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Schedule
        fields = ['name', 'user',  "date", "resource_url", "exercise", "content","start_time",
                  "end_time"]
