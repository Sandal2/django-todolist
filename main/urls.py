from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.main_page, name='main'),
    path('tasks/<int:day_pk>/', views.cur_tasks, name='tasks'),
    path('add-task/<int:day_pk>/', views.add_task, name='add_task'),
    path('change-task-status/<int:task_pk>/', views.change_task_status, name='change_status'),
    path('delete-task/<int:task_pk>/', views.delete_task, name='delete'),
]
