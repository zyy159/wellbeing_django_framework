from django.shortcuts import render
from django.http import HttpResponse,JsonResponse, Http404
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import MotionSerializer, PracticeSerializer, WorkoutSerializer, PlanSerializer

from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Motion, Practice, Workout, Plan
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, mixins
from wellbeing_django_framework.permissions import IsOwnerOrReadOnly
from rest_framework.reverse import reverse
from rest_framework import renderers


# Create your views here.
class MotionList(generics.ListCreateAPIView):
    queryset = Motion.objects.all()
    serializer_class = MotionSerializer


class MotionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Motion.objects.all()
    serializer_class = MotionSerializer


class PracticeList(generics.ListCreateAPIView):
    queryset = Practice.objects.all()
    serializer_class = PracticeSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PracticeDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Practice.objects.all()
    serializer_class = PracticeSerializer


class WorkoutList(generics.ListCreateAPIView):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class WorkoutDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer


class PlanList(generics.ListCreateAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PlanDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer


class PopularMotionList(generics.ListAPIView):
    queryset = Motion.objects.all().order_by('-popularity')[:5]
    serializer_class = MotionSerializer

