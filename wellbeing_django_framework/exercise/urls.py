from django.urls import path, re_path

from . import views
from .views import *

urlpatterns = [
    path('exercises/', ExerciseList.as_view(), name='exercise-list'),
    path('exercises/<int:pk>/', ExerciseDetail.as_view(), name='exercise-detail'),

    path('actions/', ActionList.as_view(), name='action-list'),
    path('actions/<int:pk>/', ActionDetail.as_view(), name='action-detail'),
    # path('models/', Model_storeList.as_view(), name='models-list'),
    path('model_store/<int:pk>/', Model_storeDetail.as_view(), name='model_store-detail'),
    path('model_store/', views.Model_storeList.as_view(), name='model_store-list'),
    # path('actions_list/', views.actions_list, name='actions_list'),
    # path('user_summary/', views.get_user_summary, name='user_summary'),
    path('schedules/', ScheduleList.as_view(), name='schedule-list'),
    path('schedules/<int:pk>/', ScheduleDetail.as_view(), name='schedule-detail'),

    # path('user_summary/', UserSummaryList.as_view(), name='usersummary-list'),
    path('usersummary/', UserSummaryView.as_view(), name='usersummary'),
    # path('user_summary/<int:pk>/', UserSummaryDetail.as_view(), name='usersummary-detail'),

    path('create_user/', views.create_user, name='create_user'),
    # { POST
    # "user_name": "john1",
    # "user_email": "john@example.com1",
    # "user_password": "password",
    # "user_phone": "1234567890",
    # "user_status": "active",
    # "user_type": "admin",
    # "user_group": "group1"
    # }
    path('update_user/', views.update_user, name='update_user'),
# {
#     "user_name": "john1",
#     "user_email": "john@example.com",
#     "user_old_password": "password",
#     "user_new_password": "passwordnew1",
#     "user_phone": "123456",
#     "user_status": "active",
#     "user_type": "admin",
#     "user_group": "group1"
# }
    path('logon_user/', views.logon_user, name='logon_user'),
    # { GET
    #     "user_name": "john1",
    #     "user_email": "john@example.com1",
    #     "user_password": "password"
    # }

# {
#     "event_status_choice":"not_start"
#     "user":{
#         "user_name": "john1",
#         "user_email": "john@example.com",
#         "user_old_password": "password",
#         "user_new_password": "passwordnew1",
#         "user_phone": "123456",
#         "user_status": "active",
#         "user_type": "admin",
#         "user_group": "group1"
#     },
#     "event_name":"Yogo Test01",
#     "event_motions":{
#         "motion_name":"Yogo Motion Name",
#         "motion_type":"Exercise",
#         "motion_description":"This is Yogo practice.",
#         "motion_model":{
#             "model_name":"Yogo Model",
#             "model_type":"Practice_Model",
#             "model_store_url":"https://uyhfjh.efdcd.com",
#             "model_version":1,
#         },
#     },
#     "event_start_time":"2023-05-21 09:06:37.620621+00:00",
#     "":"",
#     "":"",
#     "":"",
#     "":"",
# }
    path('create_models/', views.create_model, name='create_model'),
    # {
    #     "name": "Yogo Action001",
    #     "exercise": "Yogo",
    #     "model_url": "http://example.com/model001",
    #     "model_version": 1
    # }
    path('update_models/', views.update_models, name='update_models'),
    # {
    #     "model_name": "Example Model002",
    #     "model_type": "Type B",
    #     "model_store_url": "http://example.com/model",
    #     "model_version": 1
    # }
    path('create_exercise/', views.create_exercise, name='create_exercise'),
    # {
    #     "name": "Yogo Action001",
    #     "start_time": "Yogo",
    #     "end_time": "http://example.com/model001",
    #     "model_version": 1
    # }
    path('update_exercise/', views.update_exercise, name='update_exercise'),
    # {
    #     "id":3,
    #     "name": "Yogo",
    #     "start_time": "2023-05-21 09:06:37.620621",
    #     "end_time": "2023-05-22 09:06:37.620621"
    # }
    path('create_actions/', views.create_actions, name='create_action'),
    # {
    #     "exercise_id":3,
    #     "name": "Yogo actions"
    # }
    path('update_action/', views.update_action, name='update_action'),
    # {
    #     "id":3,
    #     "name": "Yogo Action001",
    #         "score":98,
    #         "calories":108,
    #     "start_time": "2023-05-21 09:06:37.620621",
    #     "end_time": "2023-05-22 09:06:37.620621"
    # }
    path('create_schedule/', views.create_schedule, name='create_schedule'),
    # {
    #     "schedule_name": "Stanven's Rest Time for Yogo Exercise",
    #     "exercise_name": "Yogo",
    #     "user_name": "stanven01",
    #     "user_mail": "stanven01@example.com",
    #     "schedule_content": "Please click the URL below to start your Yogo",
    #     "schedule_start_time": "2023-05-21 09:06:37.620621",
    #     "schedule_end_time": "2023-05-30 09:10:37.653323"
    # }
# {
#   "motion_name": "Example Model004",
#   "motion_type": "Training",
#   "motion_description": "Yogo motion04",
#   "motion_demo": "https://hfsdhfksahfjkhsd.com",
#   "motion_model": {
#     "model_name": "Example Model002",
#     "model_type": "Training",
#     "model_store_url": "http://example.com/model02"
#   }


]
