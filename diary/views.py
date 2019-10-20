from datetime import date
from django.shortcuts import render
from django.core import serializers
from django.contrib.auth.models import User
from diary.models import Diary
from diary.serializer import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


@api_view(['GET'])
@authentication_classes((IsAuthenticated,))
def get_diary_list(request, year=date.today().day, month=date.today().month):
    user = request.user
    diary_list = Diary.objects.filter(user=user).order_by('written')
    result = DiarySimpleSerializer(diary_list)
    
    return Response(result.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes((IsAuthenticated,))
def diary(request, pk):
    user = request.user
    diary = Diary.objects.get(id=pk)
    if diary.user != user:
        return Response({"message": "user does not match"}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        result = DiarySerializer(diary)
        return Response(result.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        fields = ('title', 'content')

        if any(i not in fields for i in data):
            return Response({"message": "invalid fields"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            diary = diary.update(**request.data)
            result = DiarySerializer(diary)
            return Response(result.data, status=status.HTTP_202_ACCEPTED)
    else:
        diary.delete()
        return Response({"message": "success"}, status=status.HTTP_202_ACCEPTED)
    

@api_view(['POST'])
@authentication_classes((IsAuthenticated,))
def post_diary(request):
    user = request.user
    if all(i in data for i in ('schedule_type', 'title', 'content', 'start_date', 'end_date')):
        data['user'] = user
        diary = Diary.objects.create(**data)
        result = DiarySerializer(diary)
        return Response(result.data, status=status.HTTP_201_CREATED)
    

    