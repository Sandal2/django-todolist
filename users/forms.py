from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class AuthenticateUserForm(AuthenticationForm):  # наследуем AuthenticationForm в AuthenticateUserForm
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))  # добавляем виджет к полю username
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))  # добавляем виджет к полю password


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))  # добавляем виджет к полю username
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))  # добавляем виджет к полю email
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))  # добавляем виджет к полю password1
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))  # # добавляем виджет к полю password2

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):  # валидатор email
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('An account with this e-mail address already exists')
        return email
