from datetime import timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from catalogue.models import (
    Locality,
    Location,
    Price,
    Representation,
    Show,
    ShowPrice,
)


class ReservationApiRegressionTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='reservation-api-user',
            password='password123',
        )
        locality = Locality.objects.create(
            postal_code='1000',
            locality='Brussels',
        )
        location = Location.objects.create(
            slug='api-location',
            designation='API Location',
            address='1 Test Street',
            locality=locality,
        )
        self.show = Show.objects.create(
            slug='api-show',
            title='API Show',
            description='API test show',
            created_in=2026,
            location=location,
        )
        self.price = Price.objects.create(
            type='adult',
            price='25.00',
            description='Adult',
            start_date='2026-01-01',
            end_date='2026-12-31',
        )
        ShowPrice.objects.create(show=self.show, price=self.price)
        self.representation = Representation.objects.create(
            show=self.show,
            location=location,
            schedule=timezone.now() + timedelta(days=1),
            available_seats=10,
            total_seats=10,
        )
        self.client.force_authenticate(user=self.user)

    def test_create_reservation_uses_through_model_and_updates_seats(self):
        response = self.client.post(
            reverse('api:reservations-list'),
            {
                'representation': self.representation.id,
                'price': self.price.id,
                'quantity': 3,
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['representation'], self.representation.id)
        self.assertEqual(response.data['quantity'], 3)
        self.representation.refresh_from_db()
        self.assertEqual(self.representation.available_seats, 7)

    def test_create_reservation_rejects_unavailable_quantity(self):
        response = self.client.post(
            reverse('api:reservations-list'),
            {
                'representation': self.representation.id,
                'price': self.price.id,
                'quantity': 11,
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Not enough seats', str(response.data))
