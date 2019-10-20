from rest_framework import serializers
from diary.models import Diary

class DiarySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ('id', 'user', 'written', 'title', 'summary')
        

class DiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ('id', 'user', 'written', 'title', 'summary', 'content')
        
        
        