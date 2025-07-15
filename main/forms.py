from django import forms
from .models import Task, Date


class AddDateForm(forms.ModelForm):
    class Meta:
        model = Date
        fields = '__all__'
        exclude = ['user']  # исключаем user из полей формы
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),  # календарь
        }


class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        exclude = ['date']  # исключаем дату из полей формы
