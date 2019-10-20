from rest_framework import serializers
from schedule.models import Schedule

class ScheduleSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ('id', 'user', 'schedule_type', 'title', 'start_date', 'end_date')
        

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ('id', 'user', 'schedule_type', 'title', 'content', 'start_date', 'end_date')
        
        
        