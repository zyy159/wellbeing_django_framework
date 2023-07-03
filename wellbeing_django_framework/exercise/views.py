import json

import pytz
import datetime as dt

from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.db.models import F
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse, Http404
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from .processers import SendAppointmentsThread
from .serializers import *
from django.core.serializers import serialize

from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import *
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, mixins
from wellbeing_django_framework.permissions import IsOwnerOrReadOnly
from rest_framework.reverse import reverse
from rest_framework import renderers
from dateutil.rrule import rrule, DAILY



# Create your views here.
class ExerciseList(generics.ListCreateAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ExerciseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

class ActionList(generics.ListCreateAPIView):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ActionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
#
class Model_storeList(generics.ListCreateAPIView):
    queryset = Model_store.objects.all()
    serializer_class = Model_storeSerializer

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)

class Model_storeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Model_store.objects.all()
    serializer_class = Model_storeSerializer

class ScheduleList(generics.ListCreateAPIView):
    queryset = Schedule.objects.all()
    serializer_class =ScheduleSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        attendee_email = self.request.user.email
        print(attendee_email)
        sub_schedule = serializer.data["sub_schedules"]
        print(sub_schedule)
        location = "front end url for starting the exercises of this schedule"
        # hardcode for testing d
        # schedule = """[{"start_time": "2023-06-22T15:00:00Z", "end_time": "2023-06-22T15:30:00Z"},
        # {"start_time": "2023-06-23T15:00:00Z", "end_time": "2023-06-23T15:30:00Z"},
        # {"start_time": "2023-06-24T15:00:00Z", "end_time": "2023-06-24T15:30:00Z"}]"""
        thread = SendAppointmentsThread(sub_schedule, attendee_email, location)
        thread.start()
        schedule = serializer.instance
        exercises = schedule.exercises.all()
        for exercise in exercises:
            exercise.popularity = exercise.popularity + 1
            exercise.save()


class ScheduleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer


# class UserSummaryList(generics.ListCreateAPIView):
#     queryset = UserSummary.objects.all()
#     serializer_class =UserSummarySerializer
#     permission_classes = (IsAuthenticated,)
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)

# class UserSummaryDetail(generics.RetrieveAPIView):
#     queryset = UserSummary.objects.all()
#     serializer_class = UserSummarySerializer
#     permission_classes = (IsAuthenticated,)


class UserSummaryView(RetrieveUpdateAPIView):
    serializer_class = UserSummarySerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        queryset = self.get_queryset()
        user = self.request.user
        if len(queryset) > 0:
            user_summary_obj = queryset[0]
        else:
            user_summary_obj = UserSummary.objects.create(
                owner = self.request.user
            )
        actionset = Action.objects.filter(owner=user)
        user_summary_obj.total_score = sum([x.score for x in actionset])
        user_summary_obj.total_calories = sum([x.calories for x in actionset])
        user_summary_obj.total_time = sum([x.end_time - x.start_time for x in actionset], dt.timedelta()).seconds
        this_month = dt.datetime.now().month
        current_month_score = 0
        current_month_calories = 0
        current_month_time = dt.datetime.now() - dt.datetime.now()
        for action in actionset:
            if action.start_time.month == this_month:
                current_month_score = current_month_score + action.score
                current_month_calories = current_month_calories + action.calories
                current_month_time = current_month_time + (action.end_time - action.start_time)

        user_summary_obj.current_month_score = current_month_score
        user_summary_obj.current_month_calories = current_month_calories
        user_summary_obj.current_month_time = current_month_time.seconds

        user_summary_obj.save()
        return user_summary_obj

    def get_queryset(self):
        """
        This view should return the user summary of current user.
        """
        user = self.request.user
        return UserSummary.objects.filter(owner=user)


# class Model_storeDetail(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
#     queryset = Model_store.objects.all()
#     serializer_class = Model_storeSerializer


# class WorkoutList(generics.ListCreateAPIView):
#     queryset = Workout.objects.all()
#     serializer_class = WorkoutSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
#
#
# class WorkoutDetail(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
#     queryset = Workout.objects.all()
#     serializer_class = WorkoutSerializer
#
#
# class EventList(generics.ListCreateAPIView):
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
#
#
# class EventDetail(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer


class PopularActionList(generics.ListAPIView):
    queryset = Model_store.objects.all().order_by('-popularity')[:5]
    serializer_class = ActionSerializer


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Wellbeing_user


@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')  # 接收前端post过来的json数据
            user_data = json.loads(body)  # 解析json数据
            ver_user_name = user_data['user_name']
            ver_user_email = user_data['user_email']

            # 检查用户名和邮箱是否已经存在
            if check_user_exists(ver_user_name, ver_user_email):
                return JsonResponse({'success': False, 'status': 'Exists'})
            else:
                pass
            # 创建用户
            Wellbeing_user.objects.create(
                user_name=user_data['user_name'],
                user_email=user_data['user_email'],
                user_password=user_data['user_password'],
                user_phone=user_data['user_phone'],
                user_status=user_data['user_status'],
                user_type=user_data['user_type'],
                last_login=timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                user_group=user_data['user_group'],
                create_time=timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                update_time=timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            )
            response_data = {
                'success': True,
                'status': 'Created',
                'user_name': user_data['user_name'],
                'user_email': user_data['user_email'],
                # 其他字段以此类推
            }
            return JsonResponse(response_data)
        except Exception as e:
            return JsonResponse({'success': False, 'status':'Error','error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Method not allowed'})

#create new user
def create_new_user(user_name,user_email):
    user=Wellbeing_user.objects.create(
        user_name=user_name,
        user_email=user_email,
        user_password="default",
        user_phone="default",
        user_status="default",
        user_type="default",
        last_login=timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
        user_group="autocreate",
        create_time=timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
        update_time=timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
    )
    user.save()
    return user
@csrf_exempt
def update_user(request):
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')  # 接收前端post过来的json数据
            user_data = json.loads(body)  # 解析json数据
            user_name = user_data['user_name']
            user_email = user_data['user_email']
            user_old_password = user_data['user_old_password']
            user_new_password = user_data['user_new_password']
            user_phone = user_data['user_phone']
            user_status = user_data['user_status']
            user_type = user_data['user_type']
            user_group = user_data['user_group']
            update_time = timezone.now().strftime('%Y-%m-%d %H:%M:%S')

            # 检查用户名和邮箱密码是否已经存在
            users = Wellbeing_user.objects.all()
            for user in users:
                if user.user_name == user_name and user.user_email == user_email:
                    #print('before update')
                    #print(user.user_email, user.user_password, user.user_phone, user.user_status, user.user_type,
                    # user.user_group, user.update_time)
                    if user_old_password: # 更新用户密码
                        if user.user_password == user_old_password:
                            user.user_password = user_new_password
                            user.save()
                            return JsonResponse({'success': True, 'status': 'Updated'})
                        else:
                            return JsonResponse({'success': True, 'status': 'PwdError'})
                    if user_phone: # 更新用户手机号
                        print(user.user_phone)
                        user.user_phone = user_phone
                    if user_status:# 更新用户状态
                        print(user.user_status)
                        user.user_status = user_status
                    if user_type: # 更新用户类型
                        print(user.user_type)
                        user.user_type = user_type
                    if user_group: # 更新用户组
                        print(user.user_group)
                        user.user_group = user_group
                    if update_time: # 更新时间
                        print(user.update_time)
                        user.update_time = update_time
                    user.save()
                    #print('after update:')
                    #print(user.user_name, user.user_email, user.user_password, user.user_phone,
                    #      user.user_type, user.user_group, user.update_time, user.user_status)
                    return JsonResponse({'success': True, 'status': 'Updated'})
                    break
            return JsonResponse({'success': True, 'status': 'NotExists'})

        except Exception as e:
            return JsonResponse({'success': False, 'status':'Error','error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Method not allowed'})



def check_user_exists(user_name, user_email):
    # 将解密后的 user_name 和 user_email 传入 filter 函数中，进行查询
    users = Wellbeing_user.objects.all()
    for user in users:
        if user.user_name == user_name and user.user_email == user_email:
            return True
            break
    return False
        # 循环完毕，未找到匹配的用户名和邮箱
        # 进行相应的处理逻辑

def retrieve_user(user_name, user_email):
    # 将解密后的 user_name 和 user_email 传入 filter 函数中，进行查询
    users = Wellbeing_user.objects.all()
    user_found=False
    for user in users:
        if user.user_name == user_name and user.user_email == user_email:
            user_found=True
            return user
            break
    if user_found is False:
        user=create_new_user(user_name,user_email)
        print(user_name+ " created")
    return user

def logon_user(request):
    if request.method == 'GET':
        try:
            body = request.body.decode('utf-8')  # 接收前端post过来的json数据
            user_data = json.loads(body)  # 解析json数据
            user_name = user_data['user_name']
            user_email = user_data['user_email']
            user_password= user_data['user_password']
            # 检查用户名和邮箱密码是否已经存在
            users = Wellbeing_user.objects.all()
            for user in users:
                if user.user_name == user_name and user.user_email == user_email :
                    if user.user_password == user_password:
                        response_data = {
                            'success': True,
                            'status': 'Exists',
                            'user_name': user_data['user_name'],
                            'user_email': user_data['user_email'],
                        }
                        return JsonResponse(response_data)
                        break
                    return JsonResponse({'success': True, 'status': 'PwdError'})
                    break
            return JsonResponse({'success': True, 'status': 'NotExists'})
        except Exception as e:
            return JsonResponse({'success': False, 'status':'Error','error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Method not allowed'})

# @csrf_exempt
# def create_event(request):
#     if request.method == 'POST':
#         try:
#             body = request.body.decode('utf-8')  # 接收前端post过来的json数据
#             user_data = json.loads(body)  # 解析json数据
#             user_name = user_data['user_name']
#             user_email = user_data['user_email']
#             event_status_choice = user_data['event_status_choice']
#             event_type_choice = user_data['event_type_choice']
#             event_title = user_data['event_title']
#             event_content = user_data['event_content']
#             event_start_time = user_data['event_start_time']
#             event_end_time = user_data['event_end_time']
#             event_create_time = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
#             event_update_time = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
#             event_create_user = user_data['event_create_user']
#             event_update_user = user_data['event_update_user']
#             event_group = user_data['event_group']
#             event_priority = user_data['event_priority']
#             event_remark = user_data['event_remark']
#             event = Event.objects.create(
#                 user_name=user_name,
#                 user_email=user_email,
#                 event_status_choice=event_status_choice,
#                 event_type_choice=event_type_choice,
#                 event_title=event_title,
#                 event_content=event_content,
#                 event_start_time=event_start_time,
#                 event_end_time=event_end_time,
#                 event_create_time=event_create_time,
#                 event_update_time=event_update_time,
#                 event_create_user=event_create_user,
#                 event_update_user=event_update_user,
#                 event_group=event_group,
#                 event_priority=event_priority,
#                 event_remark=event_remark,
#             )
#             event.save()
#             return JsonResponse({'success': True, 'status': 'Created'})
#         except Exception as e:
#             return JsonResponse({'success': False, 'status':'Error','error': str(e)})
#     else:
#         return JsonResponse({'success': False, 'error': 'Method not allowed'})

def model_store_list(request):
    queryset = Model_store.objects.all()
    serialized_data = serialize('json', queryset)
    return JsonResponse({'data': serialized_data})

def actions_list(request):
    queryset = Action.objects.all()
    serialized_data = serialize('json', queryset)
    return JsonResponse({'data': serialized_data})


def get_user_summary(request):
    if request.method == 'GET':
        try:
            body = request.body.decode('utf-8')  # 接收前端post过来的json数据
            user_data = json.loads(body)  # 解析json数据
            user_name = user_data['user_name']
            user_mail = user_data['user_mail']

            if check_user_exists(user_name, user_mail):
                user = retrieve_user(user_name, user_mail)
                schedules = Schedule.objects.filter(user=user)
                exercise_count = 0
                action_count = 0
                score_count = 0
                calories_count = 0
                for schedule in schedules:
                    #get the exercise
                    exercise = schedule.exercise
                    exercise_count =exercise_count+1
                    print(exercise)
                    actions = Action.objects.filter(exercise=exercise)
                    print("exercise : " + str(exercise_count))
                    for action in actions:
                        action_count=action_count+1
                        score_count=score_count+action.score
                        calories_count=calories_count+action.calories
                        print("score_count : " + str(score_count))
                        print("calories_count : " + str(calories_count))
                        print("actions : " + str(actions.count()))
                        print(action.id, action.name)
                return JsonResponse({'success': True,
                                     'status': 'Summary',
                                     'user_name': user_name,
                                     'user_mail': user_mail,
                                     'exercise_count': exercise_count,
                                     'action_count': action_count,
                                     'score_count': score_count,
                                     'calories_count': calories_count
                                     })
            return JsonResponse({'success': True, 'status': 'Error', 'error': 'UserNotExists'})
        except Exception as e:
            return JsonResponse({'success': False, 'status': 'Error', 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Method not allowed'})

@csrf_exempt
def create_model(request):
    if request.method =='POST':
        try:
            body = request.body.decode('utf-8')  # 接收前端post过来的json数据
            model_data = json.loads(body)  # 解析json数据
            print(model_data)
            name = model_data['name']
            exercise = model_data['exercise']
            created = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            updated = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            model_url = model_data['model_url']
            version = 1

            # 检查模型是否已经存在
            if check_model_exists(name, exercise):
                return JsonResponse({'success': False, 'status': 'Exists'})
            else:
                model_store = Model_store.objects.create(
                    name=name,
                    exercise=exercise,
                    created=created,
                    updated=updated,
                    model_url=model_url,
                    version=version,
                )
                model_store.save()
                return JsonResponse({'success': True, 'status': 'Created',"id":model_store.id})
        except Exception as e:
            return JsonResponse({'success': False, 'status': 'Error', 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Method not allowed'})

def check_model_exists(name, exercise):
    models = Model_store.objects.all()
    for mmodel in models:
        if mmodel.name == name and mmodel.exercise == exercise:
            return True
            break
    return False

@csrf_exempt
def update_models(request):
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')  # 接收前端post过来的json数据
            model_data = json.loads(body)  # 解析json数据
            name = model_data['name']
            exercise = model_data['exercise']
            model_url = model_data['model_url']
            models = Model_store.objects.all()
            for model in models:
                print(model.name,model.exercise)
                if model.name == name and model.exercise == exercise:
                    model.model_url = model_url
                    model.version = model.version+1
                    model.save()
                    print(model.version, model.model_url)
                    return JsonResponse({'success': True, 'status': 'Updated',"id":model.id})
                    break
            return JsonResponse({'success': False, 'status': 'NotExists'})
        except Exception as e:
            return JsonResponse({'success': False, 'status': 'Error', 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Method not allowed'})

@csrf_exempt
def create_exercise(request):
    if request.method =='POST':
        try:
            body = request.body.decode('utf-8')  # 接收前端post过来的json数据
            exercise_data = json.loads(body)  # 解析json数据
            print(exercise_data)
            name = exercise_data['name']
            start_time = exercise_data['start_time']
            end_time = exercise_data['end_time']
            popularity = 1
            #create the exercise without unique
            exercise = Exercise.objects.create(
                name=name,
                start_time=start_time,
                end_time=end_time,
                popularity=popularity,
            )
            exercise.save()
            return JsonResponse({'success': True, 'status': 'Created',"id":exercise.id})
        except Exception as e:
            return JsonResponse({'success': False, 'status': 'Error', 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Method not allowed'})

def sub_create_exercise(name,start_time,end_time):
    popularity = 1
    #check if the exercise exist in the models
    exercise_map_model = False
    models = Model_store.objects.all()
    for model in models:
        if model.exercise==name:
            exercise_map_model=True
            break
    if exercise_map_model:
        print("Exercise "+name + " exists in model list.")
        # create the exercise without unique
        exercise = Exercise.objects.create(
            name=name,
            start_time=start_time,
            end_time=end_time,
            popularity=popularity,
        )
        exercise.save()
        return exercise
    else:
        return None


def check_exercise_exists(name):
    exercises = Exercise.objects.all()
    for exercise in exercises:
        if exercise.name == name :
            return True
            break
    return False

@csrf_exempt
def update_exercise(request):
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')  # 接收前端post过来的json数据
            exercise_data = json.loads(body)  # 解析json数据
            print(exercise_data)
            id = exercise_data['id']
            name = exercise_data['name']
            start_time = exercise_data['start_time']
            end_time = exercise_data['end_time']
            exercises = Exercise.objects.all()
            for exercise in exercises:
                print(exercise.name)
                if exercise.name == name and exercise.id == id:
                    exercise.start_time = start_time
                    exercise.end_time = end_time
                    exercise.popularity=exercise.popularity+1
                    exercise.save()
                    return JsonResponse({'success': True, 'status': 'Updated'})
                    break
            return JsonResponse({'success': False, 'status': 'NotExists'})
        except Exception as e:
            return JsonResponse({'success': False, 'status': 'Error', 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Method not allowed'})

@csrf_exempt
def create_actions(request):
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')  # 接收前端post过来的json数据
            action_data = json.loads(body)  # 解析json数据
            print(action_data)

            exercise_id = action_data['exercise_id']
            popularity = 1

            # 获取运动对象
            exercises = Exercise.objects.filter(id=exercise_id)

            if exercises.exists():
                exercise = exercises.first()
                print(exercise)
                #models = Model_store.objects.filter(exercise__iexact=exercise.name)
                models = Model_store.objects.all()
                print("get models")
                action_counts = 0
                #this can be finetune in future
                for model in models:
                    print("model " + str(model))
                    print("exercise.name "+exercise.name)
                    print("model.exercise " + model.exercise)
                    if model and model.exercise == exercise.name:
                        action = Action.objects.create(
                            exercise=exercise,
                            name=model.name,
                            start_time=exercise.start_time,
                            end_time=exercise.end_time,
                            popularity=popularity,
                            image_url=model.model_url,
                        )
                        action.save()
                        action_counts += 1

                if action_counts > 0:
                    return JsonResponse({'success': True, 'status': 'ActionsCreated'})
                else:
                    return JsonResponse({'success': True, 'status': 'Action model does not exist'})
            else:
                return JsonResponse({'success': True, 'status': 'Exercise does not exist'})
        except Exception as e:
            return JsonResponse({'success': False, 'status': 'Error', 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Method not allowed'})

def sub_create_actions(exercise):
    actions = []
    #can be finetune in future
    models = Model_store.objects.all()
    print("get models")
    action_counts = 0
    # this can be finetune in future
    for model in models:
        if model and model.exercise == exercise.name:
            action = Action.objects.create(
                exercise=exercise,
                name=model.name,
                start_time=exercise.start_time,
                end_time=exercise.end_time,
                popularity=exercise.popularity,
                image_url=model.model_url,
            )
            action.save()
            action_counts += 1
            actions.append(action)
    return actions


@csrf_exempt
def update_action(request):
    #this use to update the action actual time, score & calories
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')  # 接收前端post过来的json数据
            action_data = json.loads(body)  # 解析json数据
            print(action_data)
            id = action_data['id']
            name = action_data['name']
            start_time = action_data['start_time']
            end_time = action_data['end_time']
            score = action_data['score']
            calories = action_data['calories']
            # this can be finetune in future
            actions = Action.objects.all()
            action_update = False
            for action in actions:
                print(action.name,action.id)
                if action.name == name and action.id == id:
                    action.start_time = start_time
                    action.end_time = end_time
                    action.popularity=action.popularity+1
                    action.score=score
                    action.calories=calories
                    action.save()
                    action_update=True
                    break
            if action_update:
                return JsonResponse({'success': True, 'status': 'ActionUpdated'})
            else:
                return JsonResponse({'success': False, 'status': 'ActionNotExists'})
        except Exception as e:
            return JsonResponse({'success': False, 'status': 'Error', 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Method not allowed'})

@csrf_exempt
def create_schedule(request):
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')  # 接收前端post过来的json数据
            schedule_data = json.loads(body)  # 解析json数据
            print(schedule_data)
            schedule_name = schedule_data['schedule_name']
            exercise_name = schedule_data['exercise_name']
            user_name = schedule_data['user_name']
            user_mail = schedule_data['user_mail']
            schedule_start_time=schedule_data['schedule_start_time']
            schedule_end_time = schedule_data['schedule_end_time']
            schedule_content = schedule_data['schedule_content']
            #check user information
            schedule_user=retrieve_user(user_name,user_mail)
            if schedule_user is not None:
                print(schedule_user)
                from datetime import datetime
                # 转换为 datetime 对象
                start_date = datetime.strptime(schedule_start_time, "%Y-%m-%d %H:%M:%S")
                end_date = datetime.strptime(schedule_end_time, "%Y-%m-%d %H:%M:%S")
                print(start_date)
                print(end_date)
                original_start_time = start_date.time()
                original_end_time = end_date.time()
                rule = rrule(
                    freq=DAILY,
                    dtstart=start_date.date(),
                    until=end_date.date()
                )
                recurring_dates = list(rule)

                # 输出重复日期
                result_dates = []
                exercise_create=False
                for date in recurring_dates:
                    print(date)
                    combined_start_datetime = datetime.combine(date, original_start_time)
                    combined_end_datetime = datetime.combine(date, original_end_time)
                    print(combined_start_datetime)
                    print(combined_end_datetime)
                    combined_date=combined_start_datetime.strftime("%Y-%m-%d %H:%M:%S") + ":" + combined_end_datetime.strftime("%Y-%m-%d %H:%M:%S") + ";"
                    result_dates.append(combined_date)
                    result_dates_string = "".join(result_dates)
                    print(result_dates)
                    # 创建新运动
                    exercise = sub_create_exercise(exercise_name, combined_start_datetime, combined_end_datetime)
                    if exercise is not None:
                        #send email to book the calendar
                        print("sendingEmail")
                        perform_send_notes(schedule_user,exercise,schedule_content)
                        print("EmailCompleted")
                        # 创建新运动的动作集
                        actions = sub_create_actions(exercise)
                        if actions is not None:
                            exercise_create = True
                        else:
                            return JsonResponse({'success': True, 'status': 'Actions does not created'})
                            break
                    else:
                        return JsonResponse({'success': True, 'status': 'Exercise does not exist in Models'})
                        break

                result_dates_string = result_dates_string.rstrip(";")
                #create the schedule
                if exercise_create:
                    schedule = Schedule.objects.create(
                        exercise=exercise,
                        name=schedule_name,
                        user=schedule_user,
                        start_time=schedule_start_time,
                        end_time=schedule_end_time,
                        date=date.today(),
                        content=schedule_content,
                        recurring_dates=result_dates_string,
                    )
                    schedule.save()
                    return JsonResponse({'success': True, 'status': 'ScheduleCreated'})
                print(result_dates)
            else:
                return JsonResponse({'success': True, 'status': 'User does not exist'})
        except Exception as e:
            return JsonResponse({'success': False, 'status': 'Error', 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Method not allowed'})

def check_schedule_exists(user,start_time):
    schedules = Schedule.objects.all()
    for schedule in schedules:
        if schedule.start_time == start_time and schedule.user== user:
            return True
            break
    return False

def check_exercise_exists(name):
    exercises = Exercise.objects.all()
    for exercise in exercises:
        if exercise.name == name :
            return True
            break
    return False

def perform_send_notes(user,exercise,exercise_url):
    # send email invitation to user after creating the Event.
    attendee_email = user.user_email
    print(attendee_email)
    calendar_schedule=[{"start_time":exercise.start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "end_time":exercise.end_time.strftime("%Y-%m-%dT%H:%M:%SZ")},]
    print(calendar_schedule)
    location = exercise_url
    # hardcode for testing d
    # schedule = """[{"start_time": "2023-06-22T15:00:00Z", "end_time": "2023-06-22T15:30:00Z"},
    # {"start_time": "2023-06-23T15:00:00Z", "end_time": "2023-06-23T15:30:00Z"},
    # {"start_time": "2023-06-24T15:00:00Z", "end_time": "2023-06-24T15:30:00Z"}]"""
    thread = SendAppointmentsThread(calendar_schedule, attendee_email, location)
    thread.start()

@csrf_exempt
def update_action(request):
    #this use to update the action actual time, score & calories
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')  # 接收前端post过来的json数据
            action_data = json.loads(body)  # 解析json数据
            print(action_data)
            id = action_data['id']
            name = action_data['name']
            start_time = action_data['start_time']
            end_time = action_data['end_time']
            score = action_data['score']
            calories = action_data['calories']
            # this can be finetune in future
            actions = Action.objects.all()
            action_update = False
            for action in actions:
                print(action.name,action.id)
                if action.name == name and action.id == id:
                    action.start_time = start_time
                    action.end_time = end_time
                    action.popularity=action.popularity+1
                    action.score=score
                    action.calories=calories
                    action.save()
                    action_update=True
                    break
            if action_update:
                return JsonResponse({'success': True, 'status': 'ActionUpdated'})
            else:
                return JsonResponse({'success': False, 'status': 'ActionNotExists'})
        except Exception as e:
            return JsonResponse({'success': False, 'status': 'Error', 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Method not allowed'})


# @csrf_exempt
# def create_motion(request):
#     if request.method =='POST':
#         try:
#             body = request.body.decode('utf-8')  # 接收前端post过来的json数据
#             motion_data = json.loads(body)  # 解析json数据
#             print(motion_data)
#             motion_name = motion_data['motion_name']
#             motion_type = motion_data['motion_type']
#             model_name = motion_data['motion_model']['model_name']
#             model_type = motion_data['motion_model']['model_type']
#             motion_description = motion_data['motion_description']
#             motion_demo = motion_data['motion_demo']
#             motion_store_url = motion_data['model_store_url']
#             motion_ready = True
#             motion_create_time = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
#             motion_popularity=1
#             # 检查动作是否已经存在
#             print(motion_name, motion_type)
#             if check_motion_exists(motion_name, motion_type):
#                 return JsonResponse({'success': False, 'status': 'MotionExists'})
#             else:
#                 motion = Motion.objects.create(
#                     motion_name=motion_name,
#                     motion_type=motion_type,
#                     motion_model=motion_data['motion_model'],
#                     motion_description=motion_description,
#                     motion_demo=motion_demo,
#                     motion_ready=motion_ready,
#                     motion_created=motion_create_time,
#                     motion_popularity=motion_popularity,
#                 )
#                 motion.save()
#                 return JsonResponse({'success': True, 'status': 'Created'})
#         except Exception as e:
#             return JsonResponse({'success': False, 'status': 'Error', 'error': str(e)})
#     else:
#         return JsonResponse({'success': False, 'error': 'Method not allowed'})
#
# def check_motion_exists(motion_name, motion_type):
#     motions = Motion.objects.all()
#
#     for motion in motions:
#         print(motion.motion_name, motion.motion_type)
#         print(motion_name, motion_type)
#         if motion.motion_name == motion_name and motion.motion_type == motion_type:
#             return True
#             break
#     return False
#

# @csrf_exempt
# def update_motion(request):
#     if request.method == 'POST':
#         try:
#             body = request.body.decode('utf-8')  # 接收前端post过来的json数据
#             motion_data = json.loads(body)  # 解析json数据
#             motion_name = motion_data['motion_name']
#             motion_type = motion_data['motion_type']
#             motion_model = motion_data['motion_model']
#             motion_description = motion_data['motion_description']
#             motion_demo = motion_data['motion_demo']
#             motion_ready = motion_data['motion_ready']
#             motion_popularity = motion_data['motion_popularity']
#             # 检查动作是否已经存在
#             print(motion_data)
#             motions = Motion.objects.all()
#             for motion in motions:
#                 if motion.motion_name == motion_name and motion.motion_type == motion_type:
#                     print('motion exists')
#                     # 检查模型是否已经存在
#                     print(motion_model)
#                     if motion_model:
#                         if check_model_exists(motion_model['model_name'], motion_model['model_type']):
#                             motion.motion_model = motion_model
#                         else:
#                             return JsonResponse({'success': False, 'status': 'ModelNotExists'})
#                             # 更新动作信息
#                         print(motion.motion_description,motion_description)
#                         if motion_description:
#                             motion.motion_description = motion_description
#                         # 更新动作信息
#                         print(motion_demo)
#                         if motion_demo:
#                             motion.motion_demo = motion_demo
#                         # 更新动作信息
#                         print(motion_ready)
#                         if motion_ready:
#                             motion.motion_ready = motion_ready
#                         # 更新动作信息
#                         print(motion_popularity)
#                         if motion_popularity:
#                             motion.motion_popularity = motion.motion_popularity + 1
#                         motion.save()
#                         print(motion.motion_popularity)
#                         return JsonResponse({'success': True, 'status': 'Updated'})
#                 else:
#                     return JsonResponse({'success': False, 'status': 'MotionNotExists'})
#                     break
#         except Exception as e:
#             return JsonResponse({'success': False, 'status': 'Error', 'error': str(e)})
#     else:
#         return JsonResponse({'success': False, 'error': 'Method not allowed'})
#
# @csrf_exempt
# def create_event(request):
#     if request.method =='POST':
#         try:
#             body = request.body.decode('utf-8')  # 接收前端post过来的json数据
#             event_data = json.loads(body)  # 解析json数据
#             print(event_data)
#             user_data = event_data['user_data']
#             event_name = event_data['event_name']
#             motion_description = event_data['motion_description']
#             event_motions = event_data['event_motions']
#             schedule = event_data['schedule']
#             motion_demo = event_data['motion_demo']
#             motion_ready = True
#             motion_create_time = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
#             motion_popularity=1
#             # 检查动作是否已经存在
#             print(motion_name, motion_type)
#             if check_motion_exists(motion_name, motion_type):
#                 return JsonResponse({'success': False, 'status': 'MotionExists'})
#             else:
#                 # 检查模型是否已经存在
#                 if check_model_exists(model_name, model_type):
#                     motion = Motion.objects.create(
#                         motion_name=motion_name,
#                         motion_type=motion_type,
#                         motion_model=motion_data['motion_model'],
#                         motion_description=motion_description,
#                         motion_demo=motion_demo,
#                         motion_ready=motion_ready,
#                         motion_created=motion_create_time,
#                         motion_popularity=motion_popularity,
#                     )
#                     motion.save()
#                     return JsonResponse({'success': True, 'status': 'Created'})
#                 else:
#                     return JsonResponse({'success': False, 'status': 'ModelNotExists'})
#         except Exception as e:
#             return JsonResponse({'success': False, 'status': 'Error', 'error': str(e)})
#     else:
#         return JsonResponse({'success': False, 'error': 'Method not allowed'})
