from rest_framework import serializers

from main.models import Date, Task


class DateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Date
        fields = ['date', 'user']


class TaskSerializer(serializers.ModelSerializer):
    date = serializers.ReadOnlyField(source='date.date')

    class Meta:
        model = Task
        fields = ['pk', 'title', 'description', 'priority', 'is_done', 'date']


class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['is_done']
