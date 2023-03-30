from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('motions/', MotionList.as_view(), name='motion-list'),
    path('motions/<int:pk>/', MotionDetail.as_view(), name='motion-detail'),
    path('practices/', PracticeList.as_view(), name='practice-list'),
    path('practices/<int:pk>/', PracticeDetail.as_view(), name='practice-detail'),
    path('workouts/', WorkoutList.as_view(), name='workout-list'),
    path('workouts/<int:pk>/', WorkoutDetail.as_view(), name='workout-detail'),
    path('plans/', PlanList.as_view(), name='plan-list'),
    path('plans/<int:pk>/', PlanDetail.as_view(), name='plan-detail'),
]