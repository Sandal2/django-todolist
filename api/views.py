from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import DateSerializer, TaskSerializer, TaskStatusSerializer
from main.models import Date, Task


class DateViewSet(ModelViewSet):
    serializer_class = DateSerializer

    def get_queryset(self):
        return Date.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        day_date = self.kwargs.get('day_date')
        return Task.objects.filter(date__date=day_date, date__user=self.request.user)

    def perform_create(self, serializer):
        day_date = self.kwargs.get('day_date')
        date_obj = Date.objects.get(date=day_date, user=self.request.user)

        serializer.save(date=date_obj)

    @action(detail=True, methods=['patch'])
    def change_status(self, request, *args, **kwargs):
        task = self.get_object()
        serializer = TaskStatusSerializer(instance=task, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        pk = instance.pk
        instance.delete()
        return Response({'message': f'Task {pk} deleted successfully'})
