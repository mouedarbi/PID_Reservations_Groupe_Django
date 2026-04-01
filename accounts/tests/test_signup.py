from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class SignUpTest(TestCase):
    def test_signup_redirect_failure(self):
        """
        Teste si l'inscription redirige correctement vers la page de login.
        Ce test devrait échouer si 'success_url' est mal configuré (NoReverseMatch).
        """
        signup_url = reverse('accounts:user-signup')
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'first_name': 'Test',
            'last_name': 'User',
            'langue': 'fr'
        }
        
        response = self.client.post(signup_url, data)
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith(reverse('accounts:login')))
