from datetime import date, timedelta
from django.shortcuts import render
from django.core import serializers
from django.db.models import Q
from django.contrib.auth.models import User
from schedule.models import Schedule
from schedule.serializer import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_schedule_list(request, year=date.today().year, month=date.today().month):
    user = request.user
    schedule_list = Schedule.objects.filter(
        user=user,
        start_date__year__gte=year,
        start_date__month__gte=month,
        start_date__year__lte=year,
        start_date__month__lte=month
    ).order_by('start_date')
    result = ScheduleSimpleSerializer(schedule_list, many=True)
    
    return Response(result.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_near_schedule(request):
    user = request.user
    today = date.today()
    tomorrow = today + timedelta(days=1)
    schedule_list = Schedule.objects.filter(
        Q(start_date__range=[today.__str__(), tomorrow.__str__()]) | 
        Q(end_date__range=[today.__str__(), tomorrow.__str__()])
    ).order_by('-start_date')
    result = ScheduleSimpleSerializer(schedule_list, many=True)

    return Response(result.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def schedule(request, pk):
    user = request.user
    data = request.data
    schedule = Schedule.objects.filter(id=pk)
    if schedule[0].user != user:
        return Response({"message": "user does not match"}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        result = ScheduleSerializer(schedule[0])
        return Response(result.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        fields = ('schedule_type', 'title', 'content', 'start_date', 'end_date')

        if any(i not in fields for i in data):
            return Response({"message": "invalid fields"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            schedule.update(**data)
            result = ScheduleSerializer(schedule[0])
            return Response(result.data, status=status.HTTP_202_ACCEPTED)
    else:
        schedule.delete()
        return Response({"message": "success"}, status=status.HTTP_202_ACCEPTED)
    

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def post_schedule(request):
    user = request.user
    data = request.data
    if all(i in data for i in ('schedule_type', 'title', 'content', 'start_date', 'end_date')):
        data['user'] = user
        schedule = Schedule.objects.create(**data)
        result = ScheduleSerializer(schedule)
        return Response(result.data, status=status.HTTP_201_CREATED)
    

    