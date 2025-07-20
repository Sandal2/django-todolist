from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Date(models.Model):
    date = models.DateField(default=timezone.now, unique=True)  # дата по умолчанию - нынешний день
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.date.strftime('%d.%m.%Y')  # вывод в формате дд.мм.гггг


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('VH', 'Very High'),
        ('H', 'High'),
        ('M', 'Medium'),
        ('L', 'Low'),
        ('VL', 'Very Low'),
    ]

    title = models.CharField(max_length=20)
    description = models.TextField(max_length=100, blank=True)
    priority = models.CharField(max_length=2, choices=PRIORITY_CHOICES, default='M')
    is_done = models.BooleanField(default=False)
    date = models.ForeignKey('Date', on_delete=models.PROTECT)

    def __str__(self):
        return self.title
