from django.conf import settings
from django.db import models
from django.utils import timezone
import decimal

User = settings.AUTH_USER_MODEL

class Cart(models.Model):
    """
    Represents a user's shopping cart. Each user has one cart.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="cart"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

    def get_total_price(self):
        """Calculates the total price of all items in the cart."""
        return sum(item.get_item_total() for item in self.items.all())

    def get_item_count(self):
        """Returns the total quantity of items in the cart."""
        return sum(item.quantity for item in self.items.all())

class CartItem(models.Model):
    """
    Represents a single item in the cart.
    Price is stored as a snapshot at the moment it is added.
    """
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )
    representation = models.ForeignKey(
        "catalogue.Representation",
        on_delete=models.CASCADE,
        related_name="cart_items"
    )
    quantity = models.PositiveIntegerField(default=1)
    price_per_item = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("cart", "representation")

    def __str__(self):
        """
        More descriptive __str__ method for better admin display and debugging.
        """
        show_title = self.representation.show.title if hasattr(self.representation, 'show') and self.representation.show else "Unknown Show"
        location_name = self.representation.location.designation if hasattr(self.representation, 'location') and self.representation.location else "Unknown Location"
        schedule_str = self.representation.schedule.strftime('%Y-%m-%d %H:%M') if self.representation.schedule else "Unknown Date"
        
        return f"{self.quantity} x '{show_title}' at {location_name} on {schedule_str}"

    def get_item_total(self):
        """
        Returns total price for this cart item.
        """
        return self.quantity * self.price_per_item