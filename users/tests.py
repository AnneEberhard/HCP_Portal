import json
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class UserAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('user_login')
        self.logout_url = reverse('user_logout')
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_user_login_success(self):
        response = self.client.post(self.login_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = json.loads(response.content)
        self.assertTrue(content['message'] == 'Login successful')

    def test_user_login_invalid_credentials(self):
        invalid_data = {'username': 'invaliduser', 'password': 'invalidpassword'}
        response = self.client.post(self.login_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        content = json.loads(response.content)
        self.assertTrue(content['error'] == 'Invalid credentials')

    def test_user_logout(self):
        # Authenticate user
        self.client.force_login(self.user)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = json.loads(response.content)
        self.assertTrue(content['message'] == 'Logout successful')
