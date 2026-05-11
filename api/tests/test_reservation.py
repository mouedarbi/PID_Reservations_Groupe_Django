from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.utils import timezone
from datetime import timedelta

from catalogue.models import Representation, Reservation, Show, Location, Locality, Price, RepresentationReservation

class ReservationsAPITests(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            email="test@example.com"
        )
        self.admin_user = User.objects.create_user(
            username="adminuser",
            password="adminpass123",
            is_staff=True
        )
        self.other_user = User.objects.create_user(
            username="otheruser",
            password="testpass123"
        )

        # Create prerequisites
        # Price
        self.price = Price.objects.create(
            type="Senior",
            price=20.0,
            description="Prix senior",
            start_date=timezone.now().date(),
            end_date=(timezone.now() + timedelta(days=365)).date()
        )

        # Show
        self.show = Show.objects.create(
            slug="test-show",
            title="Test Show",
            description="A test show",
            bookable=True,
            created_in=2024 
        )
        self.show.prices.add(self.price)
        
        # Location/Locality
        self.locality = Locality.objects.create(postal_code="1000", locality="Brussels")
        self.location = Location.objects.create(
            slug="theatre-royal",
            designation="Theatre Royal",
            address="Rue de la Loi",
            locality=self.locality
        )

        # Representation
        self.representation = Representation.objects.create(
            show=self.show,
            schedule=timezone.now() + timedelta(days=10),
            location=self.location,
            available_seats=100
        )

        # Reservation
        self.reservation = Reservation.objects.create(
            user=self.user,
            status="Confirmed"
        )
        self.rep_res = RepresentationReservation.objects.create(
            reservation=self.reservation,
            representation=self.representation,
            price=self.price,
            quantity=2
        )
        
        # Manually adjust seats
        self.representation.available_seats -= 2
        self.representation.save()

        # URLS
        self.url_list = reverse("api:reservations-list")
        self.url_detail = reverse("api:reservations-detail", kwargs={"pk": self.reservation.id})
        self.url_my = reverse("api:my-reservations")

    def test_get_reservations_list_as_admin(self):
        """Admin can list all reservations"""
        self.client.force_authenticate(user=self.admin_user)
        resp = self.client.get(self.url_list)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(len(resp.data) >= 1)

    def test_get_reservations_list_as_user(self):
        """Regular user sees nothing on the main list endpoint"""
        self.client.force_authenticate(user=self.user)
        resp = self.client.get(self.url_list)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 0)

    def test_create_reservation_authenticated(self):
        """POST /reservations/ creates a reservation and updates seats"""
        self.client.force_authenticate(user=self.user)
        initial_seats = self.representation.available_seats

        payload = {
            "representation": self.representation.id,
            "price": self.price.id,
            "quantity": 5
        }

        resp = self.client.post(self.url_list, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        
        # Check DB
        self.assertTrue(
            RepresentationReservation.objects.filter(
                reservation__user=self.user,
                representation=self.representation,
                price=self.price,
                quantity=5
            ).exists()
        )
        
        # Check Seats
        self.representation.refresh_from_db()
        self.assertEqual(self.representation.available_seats, initial_seats - 5)

    def test_create_reservation_not_enough_seats(self):
        """Should fail if requesting more seats than available"""
        self.client.force_authenticate(user=self.user)
        
        payload = {
            "representation": self.representation.id,
            "price": self.price.id,
            "quantity": 200
        }
        
        resp = self.client.post(self.url_list, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_reservation_restores_seats(self):
        """DELETE /reservations/<id>/ restores the seats"""
        self.client.force_authenticate(user=self.user)
        initial_seats = self.representation.available_seats
        quantity_to_restore = self.rep_res.quantity

        resp = self.client.delete(self.url_detail)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Reservation.objects.filter(id=self.reservation.id).exists())

        self.representation.refresh_from_db()
        self.assertEqual(self.representation.available_seats, initial_seats + quantity_to_restore)

    def test_my_reservations_endpoint(self):
        """GET /my/reservations/ returns only user's reservations"""
        self.client.force_authenticate(user=self.user)
        resp = self.client.get(self.url_my)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        
        data = resp.data['results'] if 'results' in resp.data else resp.data
        self.assertTrue(len(data) >= 1)

    def test_cannot_delete_others_reservation(self):
        """User cannot delete another user's reservation"""
        self.client.force_authenticate(user=self.other_user)
        resp = self.client.delete(self.url_detail)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
