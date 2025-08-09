from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import MainPageSerializer, TasksSerializer

from main.models import Date, Task


class MainPageAPIView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]  # ограничения доступа
    serializer_class = MainPageSerializer
    lookup_field = 'date'  # поле, по которому будет происходить поиск в get_object() (по умолчанию поиск проходит по pk)

    def get_queryset(self):
        return Date.objects.filter(user=self.request.user)

    def perform_create(self, serializer):  # переопределяем метод для привязки пользователя к дате
        serializer.save(user=self.request.user)  # по умолчанию serializer.save()

    @action(methods=['get'], detail=True)  # новый маршрут для получения задач по дате
    def tasks(self, request, date=None):
        date_obj = self.get_object()
        tasks = Task.objects.filter(date=date_obj)
        serializer = TasksSerializer(tasks, many=True)
        return Response(serializer.data)
