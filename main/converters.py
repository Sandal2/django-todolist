from datetime import datetime


class DateConverter:
    regex = r'\d{2}-\d{2}-\d{4}'  # шаблон для маршрута. django проверяет url и сопоставляет часть пути с этим regex

    def to_python(self, value):  # преобразует строку из url в объект datetime.date
        return datetime.strptime(value, '%d-%m-%Y').date()

    def to_url(self, value):  # преобразует datetime.date обратно в строку для генерации url через redirect или reverse
        return value.strftime('%d-%m-%Y')
