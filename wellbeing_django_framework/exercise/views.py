import _thread
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

from .processers import SendAppointmentsThread
from .serializers import *

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

from ..settings import EMAIL_HOST_USER


# Create your views here.
class MotionList(generics.ListCreateAPIView):
    queryset = Motion.objects.all()
    serializer_class = MotionSerializer


class MotionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Motion.objects.all()
    serializer_class = MotionSerializer
#
class VerificationList(generics.ListCreateAPIView):
    queryset = Motion.objects.all()
    serializer_class = MotionSerializer


class VerificationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Motion.objects.all()
    serializer_class = MotionSerializer
class Model_storeList(generics.ListCreateAPIView):
    queryset = Model_store.objects.all()
    serializer_class =Model_storeSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class Model_storeDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Model_store.objects.all()
    serializer_class = Model_storeSerializer


class WorkoutList(generics.ListCreateAPIView):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class WorkoutDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer


class EventList(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def perform_create(self, serializer):
        serializer.save(user=f'"{self.request.user}"')
        # send email invitation to user after creating the Event.
        attendee_email = self.request.user.email
        schedule = serializer.data["schedule"]
        location = serializer.data["event_location"]
        # hardcode for testing
        schedule = """[{"start_time": "2023-06-22T15:00:00Z", "end_time": "2023-06-22T15:30:00Z"}, 
        {"start_time": "2023-06-23T15:00:00Z", "end_time": "2023-06-23T15:30:00Z"}, 
        {"start_time": "2023-06-24T15:00:00Z", "end_time": "2023-06-24T15:30:00Z"}]"""
        thread = SendAppointmentsThread(schedule, attendee_email, location)
        thread.start()


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class PopularMotionList(generics.ListAPIView):
    queryset = Motion.objects.all().order_by('-motion_popularity')[:5]
    serializer_class = MotionSerializer


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

@csrf_exempt
def create_event(request):
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')  # 接收前端post过来的json数据
            user_data = json.loads(body)  # 解析json数据
            user_name = user_data['user_name']
            user_email = user_data['user_email']
            event_status_choice = user_data['event_status_choice']
            event_type_choice = user_data['event_type_choice']
            event_title = user_data['event_title']
            event_content = user_data['event_content']
            event_start_time = user_data['event_start_time']
            event_end_time = user_data['event_end_time']
            event_create_time = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            event_update_time = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            event_create_user = user_data['event_create_user']
            event_update_user = user_data['event_update_user']
            event_group = user_data['event_group']
            event_priority = user_data['event_priority']
            event_remark = user_data['event_remark']
            event = Event.objects.create(
                user_name=user_name,
                user_email=user_email,
                event_status_choice=event_status_choice,
                event_type_choice=event_type_choice,
                event_title=event_title,
                event_content=event_content,
                event_start_time=event_start_time,
                event_end_time=event_end_time,
                event_create_time=event_create_time,
                event_update_time=event_update_time,
                event_create_user=event_create_user,
                event_update_user=event_update_user,
                event_group=event_group,
                event_priority=event_priority,
                event_remark=event_remark,
            )
            event.save()
            return JsonResponse({'success': True, 'status': 'Created'})
        except Exception as e:
            return JsonResponse({'success': False, 'status':'Error','error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Method not allowed'})

@csrf_exempt
def create_model(request):
    if request.method =='POST':
        try:
            body = request.body.decode('utf-8')  # 接收前端post过来的json数据
            model_data = json.loads(body)  # 解析json数据
            model_name = model_data['model_name']
            model_type = model_data['model_type']
            created = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            updated = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            model_create_user = model_data['model_create_user']
            model_update_user = model_data['model_update_user']
            model_group = model_data['model_group']
            model_remark = model_data['model_remark']

            # 检查用户名和邮箱是否已经存在
            if check_model_exists(model_name, model_type):
                return JsonResponse({'success': False, 'status': 'Exists'})
            else:
                pass
        except Exception as e:
            return JsonResponse({'success': False, 'status': 'Error', 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Method not allowed'})

def check_model_exists(model_name, model_type):
    # 将解密后的 user_name 和 user_email 传入 filter 函数中，进行查询
    models = Model_store.objects.all()
    for mmodel in models:
        if mmodel.model_name == model_name and mmodel.model_type == model_type:
            return True
            break
    return False
        # 循环完毕，未找到匹配的用户名和邮箱
        # 进行相应的处理逻辑
