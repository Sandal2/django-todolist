from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from main.models import Date


class DatesAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='1234')

        token = self.client.post(reverse('api:token_obtain_pair'), {
            'username': 'tester',
            'password': '1234'
        })  # получаем токен

        self.access_token = token.data['access']  # в token.data['access'] лежит сам токен
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')  # авторизуем пользователя

    def test_create_date(self):
        data = {'date': '2025-08-10'}
        response = self.client.post(reverse('api:dates-list'), data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Date.objects.count(), 1)
        self.assertEqual(Date.objects.first().user, self.user)  # убеждаемся что дата привязана к текущему пользователю

    def test_list_dates(self):
        Date.objects.create(user=self.user, date='2025-08-10')
        response = self.client.get(reverse('api:dates-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_tasks_for_date(self):
        date_obj = Date.objects.create(user=self.user, date='2025-08-10')
        response = self.client.get(reverse('api:dates-tasks', kwargs={'date': str(date_obj.date)}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def tearDown(self):
        pass
