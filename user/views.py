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
    if all(i in data for i in ('username', 'password', 'first_name', 'last_name', 'email')):
        user_check = User.objects.filter(username=data['username'])
        email_check = User.objects.filter(email=data['email'])
        if user_check.exists(): 
            return Response({"message": "user already exists"}, status=status.HTTP_409_CONFLICT)
        elif email_check.exists():
            return Response({"message": "email already exists"}, status=status.HTTP_409_CONFLICT)
        else:
            user = User.objects.create_user(
                data['username'],
                data['email'],
                data['password'],
            )
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.save()
            return Response(model_to_dict(user), status=status.HTTP_201_CREATED)
    else:
        return Response({"message": "key error"}, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['POST'])
@authentication_classes((IsAuthenticated,))
def info_register(request):
    user = request.user
    data = request.data
    
    if Profile.objects.filter(user=user).exists():
        return Response({"message": "info already exists"}, status=status.HTTP_409_CONFLICT)
    elif all(i in data for i in ('start_date', 'end_date', 'say')):
        data['user'] = user
        profile = Profile.objects.create(**data)
        return Response(model_to_dict(profile), status=status.HTTP_201_CREATED)
    else:
        return Response({"message": "key error"}, status=status.HTTP_409_CONFLICT)


@api_view(['GET', 'PUT'])
@authentication_classes((IsAuthenticated,))
def info(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
        if request.method == "GET":
            return Response(model_to_dict(profile), status=status.HTTP_200_OK)
        else:
            fields = (
                'start_date',
                'end_date',
                'private_first_class',
                'corparal',
                'sergeant',
                'say',
                'reqular_holiday',
                'reward_holiday',
                'consolation_holiday'
            )

            if any(i not in fields for i in data):
                return Response({"message": "invaild fields"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                profile.update(**data)
                return Response({"message": "success"}, status=status.HTTP_202_ACCEPTED)

    except Profile.DoesNotExist:
        return Response({"message": "info does not exists"}, status=status.HTTP_404_NOT_FOUND)
    

