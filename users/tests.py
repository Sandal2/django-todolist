from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class RegisterTestCase(TestCase):
    def setUp(self):
        self.path = reverse('users:register')

        self.data = {
            'username': 'tester',
            'email': 'tester@gmail.com',
            'password1': 'Cfylfk!5102004_',
            'password2': 'Cfylfk!5102004_'
        }

    def test_get_register_page(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertContains(response, 'Registration')

    def test_success_registration(self):
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('main:main'))  # проверяем корректность редиректа
        self.assertTrue(User.objects.filter(username=self.data['username']).exists())  # проверяем существование юзера

    def test_password_mismatch_error(self):
        self.data['password2'] = 'Cfylfk!5102004'  # делаем так, чтобы пароли не совпадали
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'The two password fields didn’t match.')  # проверяем сообщение о несовпадении

    def test_short_password_error(self):
        self.data['password1'] = '.'
        self.data['password2'] = '.'
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'This password is too short. It must contain at least 8 characters.')

    def test_user_exists_error(self):
        User.objects.create_user(username=self.data['username'])
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'A user with that username already exists.')

    def test_email_exists_error(self):
        User.objects.create_user(username='testemail', email=self.data['email'])
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'An account with this e-mail address already exists')

    def tearDown(self):
        pass


class LoginTestCase(TestCase):
    def setUp(self):
        self.path = reverse('users:login')
        self.user = User.objects.create_user(username='tester', password='1234')

    def test_get_login_page(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertContains(response, 'Authorization')

    def test_success_authorization(self):
        response = self.client.post(self.path, {'username': 'tester', 'password': '1234'})

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('main:main'))

    def test_authorization_error(self):
        response = self.client.post(self.path, {'username': 'tester', 'password': '12345'})

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response,
                            'Please enter a correct username and password. Note that both fields may be case-sensitive.')

    def tearDown(self):
        pass
