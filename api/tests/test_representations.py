# -*- coding: utf-8 -*-
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from catalogue.models import Representation, Show, Location, Locality
from django.contrib.auth import get_user_model
from django.utils import timezone
import datetime

User = get_user_model()

class RepresentationAPITests(APITestCase):
    """
    Tests for the Representation API.
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

        cls.locality = Locality.objects.create(postal_code="1000", locality="Brussels")
        cls.location = Location.objects.create(
            slug="theatre-royal",
            designation="Théâtre Royal",
            address="Place de la Monnaie",
            locality=cls.locality
        )
        cls.show = Show.objects.create(
            slug="hamlet",
            title="Hamlet",
            created_in=2024
        )
        
        cls.now = timezone.now()
        cls.rep1 = Representation.objects.create(
            show=cls.show,
            location=cls.location,
            schedule=cls.now + datetime.timedelta(days=1),
            available_seats=50
        )
        cls.rep2 = Representation.objects.create(
            show=cls.show,
            location=cls.location,
            schedule=cls.now + datetime.timedelta(days=2),
            available_seats=20
        )

        cls.list_url = reverse('api:representations-list-create')
        cls.detail_url = reverse('api:representations-detail', kwargs={'pk': cls.rep1.id})
        cls.calendar_url = reverse('api:representations-calendar')
        cls.availability_url = reverse('api:representations-availability', kwargs={'pk': cls.rep1.id})

    def test_list_representations(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_representation(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['available_seats'], 50)

    def test_create_representation_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "show": self.show.id,
            "location": self.location.id,
            "schedule": (self.now + datetime.timedelta(days=3)).isoformat(),
            "available_seats": 100
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Representation.objects.count(), 3)

    def test_delete_representation_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Representation.objects.count(), 1)

    def test_calendar_view(self):
        start = (self.now + datetime.timedelta(hours=12)).strftime('%Y-%m-%dT%H:%M:%S')
        end = (self.now + datetime.timedelta(days=1, hours=12)).strftime('%Y-%m-%dT%H:%M:%S')
        response = self.client.get(f"{self.calendar_url}?start={start}&end={end}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_availability_view(self):
        response = self.client.get(self.availability_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['available_seats'], 50)
