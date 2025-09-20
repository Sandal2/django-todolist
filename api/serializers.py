from rest_framework import serializers

from main.models import Date, Task


class DateSerializer(serializers.Serializer):
    date = serializers.DateField()
    user = serializers.ReadOnlyField(source='user.username')

    def create(self, validated_data):
        return Date.objects.create(**validated_data)


class TaskSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    priority = serializers.ChoiceField(choices=Task.PRIORITY_CHOICES)
    is_done = serializers.BooleanField()
    date = serializers.ReadOnlyField(source='date.date')

    def create(self, validated_data):
        return Task.objects.create(**validated_data)
