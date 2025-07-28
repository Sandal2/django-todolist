from django.apps import AppConfig


class MainConfig(AppConfig):
    verbose_name = 'dj todolist main app'  # заголовок в админке
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
