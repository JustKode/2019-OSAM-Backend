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
@permission_classes((IsAuthenticated,))
def get_diary_list(request, year=date.today().year, month=date.today().month):
    user = request.user
    diary_list = Diary.objects.filter(
        user=user,
        written__year__gte=year,
        written__month__gte=month,
        written__year__lte=year,
        written__month__lte=month
    ).order_by('written')
    result = DiarySerializer(diary_list, many=True)
    
    return Response(result.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def diary(request, pk):
    user = request.user
    data = request.data
    diary = Diary.objects.filter(id=pk)
    if diary.user != user:
        return Response({"message": "user does not match"}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        result = DiarySerializer(diary[0])
        return Response(result.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        fields = ('content')

        if any(i not in fields for i in data):
            return Response({"message": "invalid fields"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            diary.update(**data)
            result = DiarySerializer(diary[0])
            return Response(result.data, status=status.HTTP_202_ACCEPTED)
    else:
        diary.delete()
        return Response({"message": "success"}, status=status.HTTP_202_ACCEPTED)
    

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def post_diary(request):
    user = request.user
    data = request.data

    if all(i in data for i in ('content', 'written')):
        if Diary.objects.filter(user=user, written=data['written']).count() != 0:
            return Response({"message": "Diary already exists"}, status=status.HTTP_403_FORBIDDEN)
        else:
            data['user'] = user
            diary = Diary.objects.create(**data)
            result = DiarySerializer(diary)
            return Response(result.data, status=status.HTTP_201_CREATED)
    

    