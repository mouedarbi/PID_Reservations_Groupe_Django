# -*- coding: utf-8 -*-
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from catalogue.models.locality import Locality
from django.contrib.auth import get_user_model

User = get_user_model()

class LocalityAPITests(APITestCase):
    """
    Tests for the Locality API.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up initial data for all tests in this class.
        """
        cls.user = User.objects.create_user(username='testuser', password='testpassword')
        cls.admin_user = User.objects.create_superuser(username='admin_test', password='adminpassword', email='admin_test@example.com')
        
        cls.locality1 = Locality.objects.create(
            postal_code="1000",
            locality="Brussels"
        )
        cls.locality2 = Locality.objects.create(
            postal_code="4000",
            locality="Liège"
        )
        
        cls.list_url = reverse('api:localities-list')
        cls.detail_url = reverse('api:localities-detail', kwargs={'id': cls.locality1.id})
        cls.invalid_detail_url = reverse('api:localities-detail', kwargs={'id': 9999})

    def test_list_localities_unauthenticated(self):
        """
        Verify that unauthenticated users cannot list localities.
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_localities_authenticated(self):
        """
        Verify that authenticated users can list localities.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_locality_unauthenticated(self):
        """
        Verify that unauthenticated users cannot retrieve a specific locality.
        """
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_locality_authenticated(self):
        """
        Verify that authenticated users can retrieve a specific locality.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['locality'], self.locality1.locality)

    def test_retrieve_non_existent_locality(self):
        """
        Verify that retrieving a non-existent locality returns a 404 Not Found.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.invalid_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_locality_unauthenticated(self):
        """
        Verify that unauthenticated users cannot create a locality.
        """
        data = {"postal_code": "5000", "locality": "Namur"}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_locality_authenticated_not_allowed(self):
        """
        Verify that authenticated users cannot create a locality as the endpoint is read-only.
        """
        self.client.force_authenticate(user=self.user)
        data = {"postal_code": "5000", "locality": "Namur"}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
