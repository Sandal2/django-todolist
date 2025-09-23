from django.urls import path, register_converter

from main.converters import DateConverter  # импортируем конвертер из main.converters
from . import views

register_converter(DateConverter, 'ddmmyyyy')

urlpatterns = [
    path('', views.DateViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('tasks/<ddmmyyyy:day_date>/', views.TaskViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('tasks/<ddmmyyyy:day_date>/<int:pk>/',
         views.TaskViewSet.as_view({'patch': 'partial_update', 'delete': 'destroy'})),
]
