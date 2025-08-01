from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView

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

    return render(request, 'main/main_page.html', {'title': 'Dates', 'days': days, 'form': form})


class CurrentTasks(ListView):
    model = Task
    template_name = 'main/tasks.html'
    context_object_name = 'tasks'  # имя переменной, под которой будет доступен список задач в шаблоне

    def get_queryset(self):  # переопределяем выводимые объекты из модели Task (по умолчанию выводятся все)
        day_date = self.kwargs['day_date']
        self.day = get_object_or_404(Date, date=day_date, user=self.request.user)  # self для повторного использования

        return Task.objects.filter(date=self.day)  # возвращаем все объекты модели Task, связанные с day

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # получаем базовый context от родительского класса

        context['title'] = 'Tasks'
        context['day'] = self.day  # передаем day для формирования ссылок

        return context  # возвращаем расширенный context для передачи в шаблон


class AddTask(FormView):
    form_class = AddTaskForm
    template_name = 'main/add_task.html'
    extra_context = {'title': 'Add Task'}

    def get_success_url(self):  # для динамических маршрутов необходимо переопределять get_success_url
        return reverse_lazy('main:tasks', kwargs={'day_date': self.kwargs['day_date']})  # перенаправляем пользователя

    def form_valid(self, form):
        day_date = self.kwargs['day_date']
        day = get_object_or_404(Date, date=day_date, user=self.request.user)

        task = form.save(commit=False)  # создаём объект модели Task из данных формы, но не сохраняем
        task.date = day  # устанавливаем связь для task с текущей датой (day)
        task.save()  # сохраняем объект модели Task в бд
        messages.success(self.request, 'Task added successfully')

        return super().form_valid(form)


def change_task_status(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk, date__user=request.user)
    task.is_done = not task.is_done
    task.save()
    messages.info(request, 'Task changed successfully')

    return redirect('main:tasks', task.date.date)


def delete_task(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk, date__user=request.user)
    date_value = task.date.date  # сохраняем значение task.date.date до удаления для редиректа
    task.delete()
    messages.warning(request, 'Task deleted successfully')

    return redirect('main:tasks', date_value)
