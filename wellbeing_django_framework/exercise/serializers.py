from rest_framework import serializers
from .models import Motion, Practice, Workout, Plan



class MotionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Motion
        fields = ['url', 'id', 'name', 'type', 'description', 'created', 'demo', 'ready']


class PracticeSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Practice
        fields = ['url', 'id', 'workout_label', 'start_time', 'end_time', 'owner', 'motion', 'score', 'calories']


class WorkoutSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Workout
        fields = ['url', 'id', 'owner', 'start_time', 'end_time', 'label', 'score', 'calories']


class PlanSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Plan
        fields = ['url', 'id', 'owner', 'name', 'motions', 'schedule']

