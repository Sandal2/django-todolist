from rest_framework import serializers

from main.models import Date, Task


class MainPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Date
        fields = '__all__'
        read_only_fields = ['id', 'user']


class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['id', 'title', 'description', 'priority', 'date', 'user']