from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
import decimal

# Import all necessary models
from catalogue.models.cart import Cart, CartItem
from catalogue.models.representation import Representation
from catalogue.models.location import Location, Locality
from catalogue.models.show import Show
from catalogue.models.price import Price

User = get_user_model()


class CartAPITestCase(APITestCase):

    def setUp(self):
        # --- Users ---
        self.user = User.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="password123"
        )
        self.other_user = User.objects.create_user(
            username="otheruser",
            email="other@test.com",
            password="password123"
        )

        # --- Login and Cart Creation ---
        self.client.login(username="testuser", password="password123")
        self.cart = Cart.objects.create(user=self.user)

        # --- Required catalogue objects ---
        self.locality = Locality.objects.create(postal_code="1000", locality="Bruxelles")
        self.location = Location.objects.create(
            slug="salle-a",
            designation="Salle A",
            address="123 Main St",
            locality=self.locality
        )
        self.show = Show.objects.create(
            slug="concert-test",
            title="Concert Test",
            created_in=2023
        )
        self.price = Price.objects.create(
            type="Adult",
            price=decimal.Decimal('25.00'),
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timezone.timedelta(days=30)
        )
        self.representation = Representation.objects.create(
            show=self.show,
            location=self.location,
            schedule=timezone.now() + timezone.timedelta(days=10),
            available_seats=10
        )
        self.representation_2 = Representation.objects.create(
            show=self.show,
            location=self.location,
            schedule=timezone.now() + timezone.timedelta(days=12),
            available_seats=5,
        )

        # --- URLs ---
        self.cart_url = reverse("api:cart-detail")
        self.cart_items_url = reverse("api:cart-item-add-update")
        self.cart_clear_url = reverse("api:cart-clear")

    # ------------------------------------------------------------------
    # CART
    # ------------------------------------------------------------------

    def test_get_cart_authenticated(self):
        """Authenticated user can retrieve their cart."""
        response = self.client.get(self.cart_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("items", response.data)

    def test_get_cart_unauthenticated(self):
        """Unauthenticated user cannot access cart."""
        self.client.logout()
        response = self.client.get(self.cart_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ------------------------------------------------------------------
    # ADD / UPDATE ITEM
    # ------------------------------------------------------------------

    def test_add_item_to_cart_and_sets_price(self):
        """User can add an item to cart and price_per_item is set correctly."""
        data = {
            "representation_id": self.representation.id,
            "quantity": 2
        }
        response = self.client.post(self.cart_items_url, data)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])

        self.cart.refresh_from_db()
        self.assertEqual(self.cart.items.count(), 1)
        cart_item = self.cart.items.first()
        self.assertEqual(cart_item.quantity, 2)
        self.assertEqual(cart_item.price_per_item, self.price.price)

    def test_update_quantity_of_existing_item(self):
        """Adding an existing representation updates its quantity in the cart."""
        self.client.post(self.cart_items_url, {"representation_id": self.representation.id, "quantity": 1})
        response = self.client.post(self.cart_items_url, {"representation_id": self.representation.id, "quantity": 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.cart.refresh_from_db()
        self.assertEqual(self.cart.items.count(), 1)
        self.assertEqual(self.cart.items.first().quantity, 3)

    def test_add_item_invalid_quantity(self):
        """Quantity must be a positive integer."""
        data = {
            "representation_id": self.representation.id,
            "quantity": -1
        }
        response = self.client.post(self.cart_items_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_item_exceeding_available_seats(self):
        """Cannot add more items than available seats."""
        data = {
            "representation_id": self.representation.id,
            "quantity": 99
        }
        response = self.client.post(self.cart_items_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ------------------------------------------------------------------
    # ITEM DETAIL
    # ------------------------------------------------------------------

    def test_get_cart_item_detail(self):
        """User can retrieve a specific cart item."""
        item = CartItem.objects.create(
            cart=self.cart,
            representation=self.representation,
            quantity=1,
            price_per_item=self.price.price
        )
        url = reverse("api:cart-item-detail", kwargs={"pk": item.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], item.id)

    def test_update_cart_item_quantity(self):
        """User can update cart item quantity."""
        item = CartItem.objects.create(
            cart=self.cart,
            representation=self.representation,
            quantity=1,
            price_per_item=self.price.price
        )
        url = reverse("api:cart-item-detail", kwargs={"pk": item.id})
        response = self.client.patch(url, {"quantity": 3}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        item.refresh_from_db()
        self.assertEqual(item.quantity, 3)

    def test_update_cart_item_quantity_exceeding_seats(self):
        """User cannot update cart item quantity beyond available seats."""
        item = CartItem.objects.create(
            cart=self.cart,
            representation=self.representation,
            quantity=1,
            price_per_item=self.price.price
        )
        url = reverse("api:cart-item-detail", kwargs={"pk": item.id})
        response = self.client.patch(url, {"quantity": 11}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        item.refresh_from_db()
        self.assertEqual(item.quantity, 1)

    def test_delete_cart_item(self):
        """User can delete a cart item."""
        item = CartItem.objects.create(
            cart=self.cart,
            representation=self.representation,
            quantity=1,
            price_per_item=self.price.price
        )
        url = reverse("api:cart-item-detail", kwargs={"pk": item.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(CartItem.objects.filter(id=item.id).exists())

    def test_user_cannot_access_other_user_cart_item(self):
        """User cannot access another user's cart items."""
        other_cart = Cart.objects.create(user=self.other_user)
        other_item = CartItem.objects.create(
            cart=other_cart,
            representation=self.representation,
            quantity=1,
            price_per_item=self.price.price
        )
        url = reverse("api:cart-item-detail", kwargs={"pk": other_item.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ------------------------------------------------------------------
    # CLEAR CART & TOTALS
    # ------------------------------------------------------------------

    def test_clear_cart(self):
        """User can clear their cart."""
        CartItem.objects.create(
            cart=self.cart,
            representation=self.representation,
            quantity=2,
            price_per_item=self.price.price
        )
        response = self.client.delete(self.cart_clear_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cart.refresh_from_db()
        self.assertEqual(self.cart.items.count(), 0)
    
    def test_cart_totals_are_correct(self):
        """Cart totals for price and items should be calculated correctly."""
        self.client.post(self.cart_items_url, {"representation_id": self.representation.id, "quantity": 2})
        self.client.post(self.cart_items_url, {"representation_id": self.representation_2.id, "quantity": 1})

        response = self.client.get(self.cart_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assuming price for representation_2 is the same for simplicity
        expected_total_price = (2 * self.price.price) + (1 * self.price.price)
        expected_total_items = 2 + 1

        self.assertEqual(decimal.Decimal(response.data['total_price']), expected_total_price)
        self.assertEqual(response.data['total_items'], expected_total_items)
