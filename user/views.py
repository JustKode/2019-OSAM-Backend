from django.shortcuts import render
from django.core import serializers
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from user.models import Profile
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


@api_view(['POST'])
def register(request):
    data = request.data
    print(data)
    if all(i in data for i in ('username', 'password', 'first_name', 'last_name', 'email')):
        user_check = User.objects.filter(username=data['username'])
        email_check = User.objects.filter(email=data['email'])
        if user_check.exists(): 
            return Response({"message": "user already exists"}, status=status.HTTP_409_CONFLICT)
        elif email_check.exists():
            return Response({"message": "email already exists"}, status=status.HTTP_409_CONFLICT)
        else:
            user = User.objects.create(**data)
            return Response(model_to_dict(user), status=status.HTTP_201_CREATED)
    else:
        return Response({"message": "key error"}, status=status.HTTP_400_BAD_REQUEST)

    

