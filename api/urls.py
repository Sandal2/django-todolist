from django.urls import path, register_converter

from main.converters import DateConverter  # импортируем конвертер из main.converters
from . import views

register_converter(DateConverter, 'ddmmyyyy')

urlpatterns = [
    path('', views.DateAPIView.as_view()),
    path('tasks/<ddmmyyyy:day_date>/', views.TaskAPIView.as_view()),
    path('tasks/<ddmmyyyy:day_date>/<int:pk>/', views.TaskAPIView.as_view()),
]
