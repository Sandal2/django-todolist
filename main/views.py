from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, FormView

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


class CurrentTasks(ListView):
    model = Task
    template_name = 'main/tasks.html'
    context_object_name = 'tasks'  # имя переменной, под которой будет доступен список задач в шаблоне

    def get_queryset(self):  # переопределяем выводимые объекты из модели Task
        day_pk = self.kwargs.get('day_pk')  # достаем параметр day_pk из self.kwargs (он приходит из маршрута)
        return Task.objects.filter(date_id=day_pk)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # получаем базовый context от родительского класса

        context['title'] = 'Tasks'
        context['day_pk'] = self.kwargs.get('day_pk')  # передаем day_pk в шаблон для формирования ссылок

        return context  # возвращаем расширенный context для передачи в шаблон


class AddTask(FormView):
    form_class = AddTaskForm
    template_name = 'main/add_task.html'

    def get_success_url(self):
        day_pk = self.kwargs.get('day_pk')  # получаем параметр day_pk из url-маршрута

        return reverse_lazy('main:tasks', kwargs={'day_pk': day_pk})  # перенаправляем пользователя

    def form_valid(self, form):
        task = form.save(commit=False)  # создаём объект модели Task из данных формы, но не сохраняем
        task.date_id = self.kwargs.get('day_pk')  # задаем внешнему ключу date_id значение day_pk
        form.save()  # сохраняем объект модели Task в бд
        messages.success(self.request, 'Task added successfully')

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'Add Task'

        return context


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
