from django.urls import path, register_converter
from . import views
from .converters import DateConverter

app_name = 'main'

register_converter(DateConverter, 'ddmmyyyy')

urlpatterns = [
    path('', views.main_page, name='main'),
    path('tasks/<ddmmyyyy:day_date>/', views.CurrentTasks.as_view(), name='tasks'),
    path('add-task/<ddmmyyyy:day_date>/', views.AddTask.as_view(), name='add_task'),
    path('change-task-status/<int:task_pk>/', views.change_task_status, name='change_status'),
    path('delete-task/<int:task_pk>/', views.delete_task, name='delete'),
]
