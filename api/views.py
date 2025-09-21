from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import DateSerializer, TaskSerializer
from main.models import Date, Task


class DateAPIView(APIView):
    def get(self, request):
        queryset = Date.objects.filter(user=request.user)
        serializer = DateSerializer(queryset, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = DateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)

        return Response(serializer.data)


class TaskAPIView(APIView):
    def get(self, request, day_date):
        queryset = Task.objects.filter(date__date=day_date)  # сравниваем day_date с полем модели date__date
        serializer = TaskSerializer(queryset, many=True)

        return Response(serializer.data)

    def post(self, request, day_date):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            date_obj = Date.objects.get(date=day_date, user=request.user)  # находим объект модели Date по дате day_date
            serializer.save(date=date_obj)  # сохраняем Task и устанавливаем для его поля date найденный объект Date

        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Method PUT is not allowed'})

        try:
            instance = Task.objects.get(pk=pk)
        except:
            return Response({'error': 'Object does not exists'})

        serializer = TaskSerializer(data=request.data, instance=instance, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data)