from datetime import date
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from main.models import Date, Task

User = get_user_model()


class MainPageTestCase(TestCase):
    def setUp(self):
        self.path = reverse('main:main')
        self.user = User.objects.create_user(username='tester', password='1234')  # создаем тестера
        self.client.force_login(self.user)

        self.existing_date = Date.objects.create(user=self.user, date=date(2025, 7, 31))

    def test_get_main_page(self):  # get-запрос
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)  # проверяем http-статус
        self.assertTemplateUsed(response, 'main/main_page.html')  # проверяем используемый шаблон
        self.assertContains(response, 'Dates')  # проверяем заголовок

    def test_get_main_page_for_anonymous_user(self):  # get-запрос со стороны неавторизованного пользователя
        self.client.logout()  # выходим из аккаунта
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn('users/login/', response.url)  # проверяем что перенаправление произошло корректно

    def test_get_data(self):  # отображение записей из бд
        response = self.client.get(self.path)
        dates = response.context['days']

        self.assertEqual(dates.count(), 1)  # проверяем кол-во задач у пользователя

    def test_get_correct_data(self):  # проверяем отображение дат только текущего пользователя
        other_user = User.objects.create_user(username='other', password='4321')  # создаем нового пользователя
        Date.objects.create(user=other_user, date=date(2025, 7, 29))  # добавляем для него дату

        response = self.client.get(self.path)
        dates = response.context['days']

        self.assertEqual(dates.count(), 1)
        self.assertIn(self.existing_date, dates)  # проверяем что existing_date есть в коллекции dates

    def test_success_add_date(self):  # отправка формы
        data = {'date': '30.07.2025'}
        response = self.client.post(self.path, data=data)  # добавляем дату (post-запрос)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)  # проверяем редирект
        self.assertTrue(
            Date.objects.filter(date=date(2025, 7, 30), user=self.user).exists())  # проверяем на наличие в бд

    def tearDown(self):
        pass


class CurrentTasksTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='1234')
        self.client.force_login(self.user)
        self.existing_date = Date.objects.create(user=self.user, date=date(2025, 7, 31))
        self.existing_task = Task.objects.create(title='test', date=self.existing_date)
        self.path = reverse('main:tasks', kwargs={'day_date': self.existing_date.date})

    def test_get_cur_tasks_page(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'main/tasks.html')
        self.assertContains(response, 'Tasks')

    def test_get_data(self):
        response = self.client.get(self.path)
        tasks = response.context['tasks']

        self.assertEqual(tasks.count(), 1)

    def test_get_correct_data(self):
        other_user = User.objects.create_user(username='other_user', password='4321')
        other_date = Date.objects.create(user=other_user, date=date(2025, 7, 30))
        Task.objects.create(title='other_task', date=other_date)

        response = self.client.get(self.path)
        tasks = response.context['tasks']

        self.assertEqual(tasks.count(), 1)
        self.assertIn(self.existing_task, tasks)

    def test_get_other_user_tasks_error(self):
        other_user = User.objects.create_user(username='other_user', password='4321')
        other_date = Date.objects.create(user=other_user, date=date(2025, 7, 30))

        response = self.client.get(reverse('main:tasks', kwargs={'day_date': other_date.date}))

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def tearDown(self):
        pass


class AddTaskTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='1234')
        self.client.force_login(self.user)
        self.existing_date = Date.objects.create(user=self.user, date=date(2025, 7, 31))
        self.path = reverse('main:add_task', kwargs={'day_date': self.existing_date.date})

    def test_get_add_task_form(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'main/add_task.html')
        self.assertContains(response, 'Add Task')

    def test_success_add_task(self):
        response = self.client.post(self.path, {'title': 'test', 'priority': 'M'})

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(Task.objects.filter(title='test', date=self.existing_date).exists())

    def tearDown(self):
        pass
