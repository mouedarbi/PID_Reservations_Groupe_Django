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
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        cls.admin_user = User.objects.create_superuser(
            username='admin_test',
            password='adminpassword',
            email='admin_test@example.com'
        )

        cls.locality1 = Locality.objects.create(
            postal_code="1000",
            locality="Brussels"
        )
        cls.locality2 = Locality.objects.create(
            postal_code="4000",
            locality="Liège"
        )

        cls.list_url = reverse('api:localities-list')
        cls.detail_url = reverse(
            'api:localities-detail',
            kwargs={'id': cls.locality1.id}
        )
        cls.invalid_detail_url = reverse(
            'api:localities-detail',
            kwargs={'id': 9999}
        )

    # ---------- LIST ----------

    def test_list_localities_unauthenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_localities_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # ---------- DETAIL ----------

    def test_retrieve_locality_unauthenticated(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_locality_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['locality'],
            self.locality1.locality
        )

    def test_retrieve_non_existent_locality(self):
        response = self.client.get(self.invalid_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ---------- CREATE ----------

    def test_create_locality_unauthenticated(self):
        data = {"postal_code": "5000", "locality": "Namur"}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_locality_authenticated_non_admin(self):
        self.client.force_authenticate(user=self.user)
        data = {"postal_code": "5000", "locality": "Namur"}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_locality_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {"postal_code": "5000", "locality": "Namur"}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # ---------- UPDATE (PUT) ----------

    def test_update_locality_unauthenticated(self):
        data = {"postal_code": "1001", "locality": "Brussels-City"}
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_locality_authenticated_non_admin(self):
        self.client.force_authenticate(user=self.user)
        data = {"postal_code": "1001", "locality": "Brussels-City"}
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_locality_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {"postal_code": "1001", "locality": "Brussels-City"}
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.locality1.refresh_from_db()
        self.assertEqual(self.locality1.locality, "Brussels-City")

    # ---------- UPDATE (PATCH) ----------

    def test_partial_update_locality_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {"locality": "Bruxelles"}
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.locality1.refresh_from_db()
        self.assertEqual(self.locality1.locality, "Bruxelles")
        self.assertEqual(self.locality1.postal_code, "1000") # Ensure other fields are unchanged

    # ---------- DELETE ----------

    def test_delete_locality_unauthenticated(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_locality_authenticated_non_admin(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_locality_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Locality.objects.filter(id=self.locality1.id).exists())