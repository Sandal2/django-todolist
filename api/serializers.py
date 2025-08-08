from rest_framework import serializers

from main.models import Date


class MainPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Date
        fields = '__all__'
        read_only_fields = ['id', 'user']