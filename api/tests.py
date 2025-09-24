from datetime import date
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from main.models import Date, Task

User = get_user_model()


class DateViewSetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='1234')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.path = reverse('api:dates')

    def test_get_dates(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_dates_for_anonymous_user(self):
        self.client.logout()
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_add_date(self):
        data = {'date': '2025-09-23'}
        response = self.client.post(self.path, data, format='json')

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertTrue(Date.objects.filter(date='2025-09-23', user=self.user).exists())


class TaskViewSetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='1234')
        self.other_user = User.objects.create_user(username='other', password='1234')

        self.client = APIClient()
        self.client.force_authenticate(self.user)

        self.date = Date.objects.create(date='2025-09-23', user=self.user)
        self.other_date = Date.objects.create(date='2025-09-23', user=self.other_user)

        self.path = reverse('api:tasks', kwargs={'day_date': date(2025, 9, 23)})

    def test_list_tasks(self):
        Task.objects.create(title="Task 1", date=self.date)
        Task.objects.create(title="Task 2", date=self.date)
        Task.objects.create(title="Other user task", date=self.other_date)

        response = self.client.get(self.path)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        titles = [task['title'] for task in response.json()]
        self.assertIn('Task 1', titles)
        self.assertIn('Task 2', titles)
        self.assertNotIn("Other user task", titles)

    def test_create_task(self):
        data = {'title': 'New Task'}
        response = self.client.post(self.path, data, format='json')

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertTrue(Task.objects.filter(title='New Task', date=self.date).exists())

    def test_change_status(self):
        task = Task.objects.create(title='Task to update', date=self.date)
        url = reverse('api:tasks-detail', kwargs={'day_date': date(2025, 9, 23), 'pk': task.pk})

        response = self.client.patch(url, {'is_done': True}, format='json')
        self.assertEqual(response.status_code, HTTPStatus.OK)

        task.refresh_from_db()
        self.assertTrue(task.is_done)

    def test_delete_task(self):
        task = Task.objects.create(title='Task to delete', date=self.date)
        url = reverse('api:tasks-detail', kwargs={'day_date': date(2025, 9, 23), 'pk': task.pk})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())

    def test_get_tasks_for_other_user(self):
        task = Task.objects.create(title='Other users task', date=self.other_date)
        url = reverse('api:tasks-detail', kwargs={'day_date': date(2025, 9, 23), 'pk': task.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
