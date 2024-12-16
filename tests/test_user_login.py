from django.test import TestCase, Client
from django.urls import reverse


class TestLoginView(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_view_get(self):
        response = self.client.get(reverse('web:login'))
        self.assertEqual(response.status_code, 200)

    def test_login_view_post_success(self):
        data = {
            'username': 'andi@andi.com',
            'password': '12345'
        }
        response = self.client.post(reverse('web:login'), data)
        self.assertEqual(response.status_code, 302)

    def test_login_view_post_failed(self):
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(reverse('web:login'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Username atau password salah')
