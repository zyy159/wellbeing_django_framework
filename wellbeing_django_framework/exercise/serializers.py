from rest_framework import serializers
from .models import *
import datetime as dt



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
    calories = serializers.SerializerMethodField('get_calories')

    def get_calories(self, obj):
        return sum([x.calories for x in obj.model_stores.all()])

    class Meta:
        model = Exercise
        fields = ['url', 'id','name', 'duration', 'popularity', 'calories', 'category', 'model_stores']

class ActionSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Action
        fields = ['url', 'id', 'owner', 'model_store', "start_time", "end_time", "score", "calories", "label"]

class Model_storeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Model_store
        fields = ['url', 'id', 'name', 'description', 'duration', 'category',  "model_url", "created", "modified", "popularity", 'calories', "version"]

class ScheduleSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Schedule
        fields = ['url', 'id', 'name', 'owner', 'exercises', "start_time", "end_time", "sub_schedules", "location"]


class UserSummarySerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    email = serializers.ReadOnlyField(source='owner.email')
    wellbeing_level = serializers.SerializerMethodField('get_wellbeing_level')
    total_time = serializers.SerializerMethodField('get_total_time')
    current_month_time = serializers.SerializerMethodField('get_current_month_time')

    def get_wellbeing_level(self, obj):
        return int(obj.total_time/60/10)

    def get_total_time(self, obj):
        return str(dt.timedelta(seconds=obj.total_time))

    def get_current_month_time(self, obj):
        return str(dt.timedelta(seconds=obj.current_month_time))

    class Meta:
        model = UserSummary
        fields = ['id', 'owner', 'email', "wellbeing_level", 'total_score', "total_calories", "total_time", 'current_month_score', "current_month_calories",
                  "current_month_time"]


class RewardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Reward
        fields = ['url', 'id', 'name', 'description', 'image_url', 'points']


class BadgeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Badge
        fields = ['url', 'id', 'name', 'description', 'image_url', 'points']


class UserRewardSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = UserReward
        fields = ['url', 'id', 'owner', 'reward', 'reward_points', 'reward_date']


class UserBadgeSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = UserBadge
        fields = ['url', 'id', 'owner', 'badge', 'badge_points', 'badge_date']


class UserPointsSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = PointRecord
        fields = ['url', 'id', 'owner', 'points', 'remark', 'points_date']


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    email = serializers.CharField(source='owner.email')
    likes_received = serializers.CharField(source='owner.likes_received.count')
    likers = serializers.SerializerMethodField('get_likers')
    likees = serializers.SerializerMethodField('get_likees')
    total_score = serializers.ReadOnlyField(source='owner.usersummary.total_score')
    total_calories = serializers.ReadOnlyField(source='owner.usersummary.total_calories')
    total_time = serializers.ReadOnlyField(source='owner.usersummary.total_time')
    invitees = serializers.SerializerMethodField('get_invitees')

    class Meta:
        model = Profile
        fields = ['id', 'owner', 'email', 'points', 'used_points', 'badge', 'likes_received', 'likers', 'likees', 'total_score', 'total_calories', 'total_time', 'invite_code', 'invitees']

    def get_likers(self, obj):
        return [like.liker.id for like in obj.owner.likes_received.all()]

    def get_likees(self, obj):
        return [like.likee.id for like in obj.owner.likes_given.all()]

    def get_invitees(self, obj):
        return [invite.invitee.username for invite in obj.owner.invites_sent.all()]


class UserListSerializer(serializers.HyperlinkedModelSerializer):
    points = serializers.IntegerField(source='profile.points')
    badge = serializers.CharField(source='profile.badge.image_url')
    total_score = serializers.IntegerField(source='usersummary.total_score')
    total_calories = serializers.IntegerField(source='usersummary.total_calories')
    total_time = serializers.IntegerField(source='usersummary.total_time')
    likes_received = serializers.IntegerField(source='likes_received.count')
    invites_sent = serializers.IntegerField(source='invites_sent.count')

    class Meta:
        model = User
        fields = ['pk', 'username', 'points', 'badge', 'total_score', 'total_calories', 'total_time', 'likes_received', 'invites_sent']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

class InviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invite
        fields = ['code']

