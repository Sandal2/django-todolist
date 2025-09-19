# 1. Базовый образ Python
FROM python:3.12-slim

# 2. Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 3. Рабочая директория
WORKDIR /app

# 4. Копируем файлы зависимостей
COPY requirements.txt .

# 5. Устанавливаем зависимости Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 6. Копируем проект
COPY . .

# 7. Команда для запуска Django
CMD ["gunicorn", "todolist.wsgi:application", "--bind", "0.0.0.0:8000"]
