from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from main.forms import AddTaskForm, AddDateForm
from main.models import Task, Date


@login_required
def main_page(request):
    days = Date.objects.filter(user=request.user)  # извлекаем все объекты Date текущего авторизованного пользователя

    if request.method == 'POST':
        form = AddDateForm(request.POST)
        if form.is_valid():
            date = form.save(commit=False)  # создаём объект модели Date из данных формы, но не сохраняем
            date.user = request.user  # привязываем текущего авторизованного пользователя к полю user модели Date
            date.save()  # сохраняем объект модели Date в бд
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
            task = form.save(commit=False)  # создаём объект модели Task из данных формы, но не сохраняем
            task.date_id = day_pk  # задаем внешний ключ date_id значение day_pk
            task.save()  # сохраняем объект модели Task в бд
            messages.success(request, 'Task added successfully')
            return redirect('main:tasks', day_pk)
    else:
        form = AddTaskForm()

    return render(request, 'main/add_task.html', {'title': 'Add Task', 'form': form})


def change_task_status(request, task_pk):
    task = Task.objects.get(pk=task_pk, date__user=request.user)
    task.is_done = not task.is_done
    task.save()
    messages.info(request, 'Task changed successfully')

    return redirect('main:tasks', task.date.pk)  # извлекаем pk объекта Date и передаём в маршрут tasks


def delete_task(request, task_pk):
    task = Task.objects.get(pk=task_pk, date__user=request.user)
    day_pk = task.date.pk  # присваиваем переменной day_pk pk объекта Date до удаления task
    task.delete()
    messages.warning(request, 'Task deleted successfully')

    return redirect('main:tasks', day_pk)
