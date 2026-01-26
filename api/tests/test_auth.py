from django.contrib.auth.models import User, Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

class AuthAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create user group
        Group.objects.create(name='MEMBER')

        # URLs
        cls.signup_url = reverse('api:auth-signup')
        cls.login_url = reverse('api:auth-login')
        cls.logout_url = reverse('api:auth-logout')

        # Test user data
        cls.user_data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'langue': 'en'
        }

    def test_signup_success(self):
        """
        Ensure a new user can be created successfully.
        """
        response = self.client.post(self.signup_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertTrue(Token.objects.filter(user__username='testuser').exists())
        self.assertIn('token', response.data)

    def test_signup_missing_field(self):
        """
        Ensure signup fails if a required field is missing.
        """
        data = self.user_data.copy()
        del data['email']
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_existing_username(self):
        """
        Ensure signup fails if the username already exists.
        """
        User.objects.create_user(username='testuser', password='password')
        response = self.client.post(self.signup_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        """
        Ensure a user can log in with correct credentials.
        """
        User.objects.create_user(username=self.user_data['username'], password=self.user_data['password'])
        login_data = {'username': self.user_data['username'], 'password': self.user_data['password']}
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_wrong_credentials(self):
        """
        Ensure login fails with incorrect credentials.
        """
        User.objects.create_user(username=self.user_data['username'], password=self.user_data['password'])
        login_data = {'username': self.user_data['username'], 'password': 'wrongpassword'}
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_success(self):
        """
        Ensure an authenticated user can log out.
        """
        user = User.objects.create_user(username=self.user_data['username'], password=self.user_data['password'])
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Token.objects.filter(user=user).exists())

    def test_logout_unauthenticated(self):
        """
        Ensure an unauthenticated user cannot log out.
        """
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
