from django.urls import path, re_path

from . import views
from .views import *

urlpatterns = [
    path('motions/', MotionList.as_view(), name='motion-list'),
    path('motions/<int:pk>/', MotionDetail.as_view(), name='motion-detail'),
    path('popular_motions/', PopularMotionList.as_view(), name='popular-motion-list'),
    path('practices/', Model_storeList.as_view(), name='practice-list'),
    path('practices/<int:pk>/', Model_storeList.as_view(), name='practice-detail'),
    path('workouts/', WorkoutList.as_view(), name='workout-list'),
    path('workouts/<int:pk>/', WorkoutDetail.as_view(), name='workout-detail'),
    path('events/', Model_storeList.as_view(), name='plan-list'),
    path('events/<int:pk>/', WorkoutDetail.as_view(), name='plan-detail'),
    path('verification/', VerificationList.as_view(), name='verification-list'),
    path('verification/<int:pk>/', VerificationDetail.as_view(), name='verification -detail'),
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
]
