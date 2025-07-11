from django.contrib import messages
from django.shortcuts import render, redirect

from main.forms import AddTaskForm, AddDateForm
from main.models import Task, Date


def main_page(request):
    days = Date.objects.all()  # извлекаем все объекты Date

    if request.method == 'POST':
        form = AddDateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:main')
    else:
        form = AddDateForm()

    return render(request, 'main/main_page.html', {'title': 'Tasks', 'days': days, 'form': form})


def cur_tasks(request, day_pk):
    tasks = Task.objects.filter(date_id=day_pk)

    return render(request, 'main/tasks.html', {'title': 'Tasks', 'tasks': tasks, 'day_pk': day_pk})


def add_task(request, day_pk):
    if request.method == 'POST':
        form = AddTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)  # создаём объект модели (Task) из данных формы, но не сохраняем
            task.date_id = day_pk  # задаем внешний ключ date_id значение day_pk
            task.save()  # сохраняем объект модели (Task) в бд
            messages.success(request, 'Task added succesfully')
            return redirect('main:tasks', day_pk)
    else:
        form = AddTaskForm()

    return render(request, 'main/add_task.html', {'title': 'Add Task', 'form': form})


def change_task_status(request, task_pk):
    task = Task.objects.get(pk=task_pk)
    task.is_done = not task.is_done
    task.save()
    messages.info(request, 'Task changed successfully')

    return redirect('main:tasks', task.date.pk)  # извлекаем pk объекта Date и передаём в маршрут tasks


def delete_task(request, task_pk):
    task = Task.objects.get(pk=task_pk)
    task.delete()
    messages.warning(request, 'Task deleted successfully')

    return redirect('main:tasks', task.date.pk)  # извлекаем pk объекта Date и передаём в маршрут tasks
