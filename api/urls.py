from django.urls import path, register_converter

from main.converters import DateConverter  # импортируем конвертер
from . import views

register_converter(DateConverter, 'ddmmyyyy')  # регистрируем конвертер

urlpatterns = [
    path('', views.DateAPIView.as_view()),
    path('tasks/<ddmmyyyy:day_date>/', views.TaskAPIView.as_view())  # добавляем эндпоинт для тасков в формате ддммгггг
]
