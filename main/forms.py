from django import forms
from .models import Task, Date


class AddDateForm(forms.ModelForm):
    class Meta:
        model = Date
        fields = '__all__'
        exclude = ['user']  # исключаем user из полей формы
        widgets = {
            'date': forms.DateInput(attrs={
                'class': 'form-control flatpickr text-center',  # делаем календарь с помощью flatpickr
                'placeholder': 'Select a date',
            }),
        }


class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        exclude = ['date']  # исключаем дату из полей формы
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter task title',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter task description',
            }),
            'priority': forms.Select(attrs={
                'class':'form-select',
            }),
            'is_done': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
