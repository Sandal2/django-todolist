from rest_framework import serializers

from main.models import Date, Task


class DateSerializer(serializers.Serializer):
    date = serializers.DateField()
    user = serializers.ReadOnlyField(source='user.username')

    def create(self, validated_data):
        return Date.objects.create(**validated_data)


class TaskSerializer(serializers.Serializer):
    pk = serializers.ReadOnlyField()
    title = serializers.CharField()
    description = serializers.CharField(allow_blank=True, required=False)
    priority = serializers.ChoiceField(choices=Task.PRIORITY_CHOICES)
    is_done = serializers.BooleanField()
    date = serializers.ReadOnlyField(source='date.date')

    def create(self, validated_data):
        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.is_done = validated_data.get('is_done', instance.is_done)
        instance.save()

        return instance