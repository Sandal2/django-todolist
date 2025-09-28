````markdown
# Django ToDoList

Простое приложение ToDo с веб-интерфейсом и REST API на Django + DRF.  
Проект включает регистрацию/вход пользователей, хранение «дат» (Date) и задач (Task) для каждой даты, набор тестов и docker-compose для локального/контейнерного запуска.

---

## Стек технологий
- Python 3.12
- Django 5.2.3
- Django REST Framework 3.16.1
- PostgreSQL 16
- Gunicorn
- Docker / Docker Compose
- flatpickr (календарь в UI)
- Bootstrap 5

---

## Быстрый старт (Docker)

> **Важно**: в `docker-compose.yml` сервис `web` использует `env_file: .env`.  
> Для корректной работы в Docker значение `DB_HOST` в `.env` должно быть `db` (имя сервиса в compose). См. раздел «Нюансы» ниже.

1. Сборка и запуск:
```bash
docker-compose up --build -d
````

2. Выполнить миграции:

```bash
docker-compose exec web python manage.py migrate
```

3. Создать суперпользователя (для доступа к /admin/):

```bash
docker-compose exec web python manage.py createsuperuser
```

4. Открыть приложение:

* Веб-интерфейс: `http://localhost:8000/`
* Админка: `http://localhost:8000/admin/`
* API: `http://localhost:8000/api/`

---

## Локальный запуск без Docker

1. Создать venv и активировать:

```bash
python -m venv venv
# Linux / macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
```

2. Установить зависимости:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

3. Создать файл `.env` (пример ниже), настроить переменные окружения.

4. Применить миграции и запустить:

```bash
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

---

## Пример `.env`

**Для Docker (рекомендовано):**

```
DJANGO_SECRET_KEY=ваш_секретный_ключ
DEBUG=False
DB_NAME=todolist_db
DB_USER=todolist
DB_PASSWORD=1234
DB_HOST=db
DB_PORT=5432
ALLOWED_HOSTS=127.0.0.1,localhost
```

**Для локального запуска (без Docker, Postgres установлен на хосте):**

```
DB_HOST=localhost
```

---

## Маршруты / Endpoints

### Веб

* `/` — главная страница со списком дат.
* `/tasks/<dd-mm-YYYY>/` — список задач на дату.
* `/add-task/<dd-mm-YYYY>/` — форма добавления задачи.
* `/change-task-status/<id>/` — переключение статуса задачи (POST).
* `/delete-task/<id>/` — удаление задачи (POST).

### Аутентификация

* `/users/login/`
* `/users/logout/`
* `/users/register/`

### REST API

* `GET /api/` — список дат пользователя.
* `POST /api/` — создать дату. JSON: `{"date": "YYYY-MM-DD"}`.
* `GET /api/tasks/<dd-mm-YYYY>/` — список задач на дату.
* `POST /api/tasks/<dd-mm-YYYY>/` — создать задачу. JSON: `{"title": "Task", "description": "...", "priority": "M"}`.
* `PATCH /api/tasks/<dd-mm-YYYY>/<id>/` — обновить задачу (например, `is_done`).
* `DELETE /api/tasks/<dd-mm-YYYY>/<id>/` — удалить задачу.

**Аутентификация API:** BasicAuth (логин/пароль Django) или сессионные куки. JWT в проекте **нет**.

---

## Примеры cURL

Получить даты:

```bash
curl -u username:password http://localhost:8000/api/
```

Создать дату:

```bash
curl -u username:password -H "Content-Type: application/json" \
  -d '{"date":"2025-09-23"}' -X POST http://localhost:8000/api/
```

Список задач:

```bash
curl -u username:password http://localhost:8000/api/tasks/23-09-2025/
```

Создать задачу:

```bash
curl -u username:password -H "Content-Type: application/json" \
  -d '{"title":"New Task","priority":"M"}' -X POST http://localhost:8000/api/tasks/23-09-2025/
```

Обновить статус:

```bash
curl -u username:password -H "Content-Type: application/json" \
  -d '{"is_done":true}' -X PATCH http://localhost:8000/api/tasks/23-09-2025/1/
```

---

## Тесты

Локально:

```bash
python manage.py test
```

В Docker:

```bash
docker-compose run --rm web python manage.py test
```

---

## Нюансы

1. **Форматы даты**:

   * В формах: `DD.MM.YYYY`
   * В URL: `DD-MM-YYYY`
   * В API JSON: `YYYY-MM-DD`

2. **DB_HOST**:

   * В Docker: `db`
   * Локально: `localhost`

3. **DEBUG**:
   В `settings.py` `DEBUG` берётся как строка. Рекомендуется преобразовывать в булево:

   ```python
   DEBUG = os.getenv('DEBUG', 'False').lower() in ('1', 'true', 'yes')
   ```

---

## Структура проекта

```
todolist/
├── api/        # DRF viewsets, serializers, urls, тесты API
├── main/       # веб-часть: шаблоны, формы, модели, тесты
├── users/      # аутентификация и тесты
├── todolist/   # settings, urls, wsgi
├── templates/
├── static/
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

```
```
