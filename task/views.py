from django.shortcuts import render
from django.contrib.auth.models import User
from task.serializers import  UserSerializer ,UserProfileSerializer

from rest_framework import viewsets
from .models import UserProfile
from .serializers import UserProfileSerializer



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

