from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from wellbeing_django_framework.serializers import UserSerializer, GroupSerializer

def login(request):
    username = request.POST["Username"];
    password = request.POST["Password"];
    return HttpResponse("True")

def register(request):
    username = request.POST["Username"];
    password = request.POST["Password"];
    email = request.POST["Email"];
    return HttpResponse("True")


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]