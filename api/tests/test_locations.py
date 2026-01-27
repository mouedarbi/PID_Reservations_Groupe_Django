# -*- coding: utf-8 -*-
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from catalogue.models.location import Location
from catalogue.models.locality import Locality
from django.contrib.auth import get_user_model

User = get_user_model()


class LocationAPITests(APITestCase):
    """
    Tests for the Location API.
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

        cls.locality = Locality.objects.create(
            postal_code="1000",
            locality="Brussels"
        )
        cls.location1 = Location.objects.create(
            slug="theatre-de-la-monnaie",
            designation="Théâtre Royal de la Monnaie",
            address="Place de la Monnaie, 1000 Bruxelles",
            locality=cls.locality
        )
        cls.location2 = Location.objects.create(
            slug="bozar",
            designation="Bozar",
            address="Rue Ravenstein 23, 1000 Bruxelles",
            locality=cls.locality
        )

        cls.list_url = reverse('api:locations-list-create')
        cls.detail_url = reverse(
            'api:locations-detail',
            kwargs={'pk': cls.location1.id}
        )
        cls.invalid_detail_url = reverse(
            'api:locations-detail',
            kwargs={'pk': 9999}
        )

    # ---------- LIST ----------

    def test_list_locations_unauthenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_locations_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_locations_filtered_by_locality(self):
        # Create another locality and location to ensure filtering works
        other_locality = Locality.objects.create(postal_code="4000", locality="Liège")
        Location.objects.create(slug="forum", designation="Le Forum", address="Rue Pont d'Avroy 14", locality=other_locality)
        
        response = self.client.get(f"{self.list_url}?locality_id={self.locality.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['designation'], self.location1.designation)

    # ---------- DETAIL ----------

    def test_retrieve_location_unauthenticated(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['designation'], self.location1.designation)

    def test_retrieve_non_existent_location(self):
        response = self.client.get(self.invalid_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ---------- CREATE ----------

    def test_create_location_unauthenticated(self):
        data = {"slug": "new-loc", "designation": "New Location", "locality_id": self.locality.id}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_location_authenticated_non_admin(self):
        self.client.force_authenticate(user=self.user)
        data = {"slug": "new-loc", "designation": "New Location", "locality_id": self.locality.id}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_location_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {"slug": "new-loc", "designation": "New Location", "address": "Some Address", "locality": self.locality.id}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Location.objects.filter(slug="new-loc").exists())

    # ---------- UPDATE ----------

    def test_update_location_unauthenticated(self):
        data = {"designation": "Updated Name"}
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_location_authenticated_non_admin(self):
        self.client.force_authenticate(user=self.user)
        data = {"designation": "Updated Name"}
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_location_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "slug": "theatre-de-la-monnaie-updated",
            "designation": "Updated Théâtre Royal de la Monnaie",
            "address": "Updated Address",
            "locality": self.locality.id
        }
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.location1.refresh_from_db()
        self.assertEqual(self.location1.designation, "Updated Théâtre Royal de la Monnaie")

    def test_partial_update_location_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {"designation": "Partially Updated Name"}
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.location1.refresh_from_db()
        self.assertEqual(self.location1.designation, "Partially Updated Name")

    # ---------- DELETE ----------

    def test_delete_location_unauthenticated(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_location_authenticated_non_admin(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_location_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Location.objects.filter(id=self.location1.id).exists())
