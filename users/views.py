from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import FormView

from users.forms import RegisterUserForm, AuthenticateUserForm


class LoginUser(LoginView):
    form_class = AuthenticateUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Authorization', 'hide_navbar': True}  # убираем navbar в шаблоне


class RegisterUser(FormView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {
        'title': 'Registration',
        'hide_navbar': True  # убираем navbar в шаблоне
    }
    success_url = reverse_lazy('main:main')  # нужен ли нам success_url тут?

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # авторизуем пользователя сразу после регистрации

        return super().form_valid(form)
