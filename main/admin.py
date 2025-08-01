from django.contrib import admin

from .models import Date, Task


@admin.register(Date)  # регистрируем модель Date в админке через декоратор
class DateAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'user')  # отображаемые поля в админке
    list_display_links = ('id', 'date')  # делаем id и date кликабельными в админке

    readonly_fields = ['date', 'user']  # нередактируемые поля


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'priority', 'is_done', 'date', 'get_username')
    list_display_links = ('id', 'title')
    list_editable = ('is_done',)  # делаем поле is_done изменяемым в админке (должен передаваться кортеж)
    list_per_page = 10  # пагинация
    list_filter = ['is_done', 'priority']  # поля для поиска по фильтру

    readonly_fields = ['date']
    search_fields = ['title']  # поиск по title

    def get_username(self, obj: Task):  # obj является текущим объектом модели Date
        return obj.date.user.username  # обращаемся к полю username через obj(текущий экземпляр модели Date).date.user.username

    get_username.short_description = 'User'  # задаём заголовок для колонки в админке
