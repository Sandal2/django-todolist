from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect

from users.forms import RegisterUserForm, AuthenticateUserForm


class LoginUser(LoginView):
    form_class = AuthenticateUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Authorization', 'hide_navbar': True}  # убираем navbar в шаблоне


def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # авторизуем пользователя сразу после регистрации
            return redirect('main:main')
    else:
        form = RegisterUserForm()

    return render(request, 'users/register.html', {'title': 'Registration', 'form': form, 'hide_navbar': True})
