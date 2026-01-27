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
        related_name="cart",
        primary_key=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

    def get_total_price(self):
        """Calculates the total price of all items in the cart."""
        total = sum(item.get_item_total() for item in self.items.all())
        return total

    def get_item_count(self):
        """Returns the total number of individual items across all cart items."""
        return sum(item.quantity for item in self.items.all())

class CartItem(models.Model):
    """
    Represents a single item within a user's cart.
    This item is linked to a specific show representation and includes quantity and price.
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
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2) 
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("cart", "representation") 

    def __str__(self):
        show_title = self.representation.show.title if hasattr(self.representation, 'show') and self.representation.show else "Unknown Show"
        location_name = self.representation.location.designation if hasattr(self.representation, 'location') and self.representation.location else "Unknown Location"
        schedule_str = self.representation.schedule.strftime('%Y-%m-%d %H:%M') if self.representation.schedule else "Unknown Date"
        
        return f"{self.quantity} x '{show_title}' at {location_name} on {schedule_str}"

    def get_item_total(self):
        """Calculates the total price for this cart item (quantity * price_per_item)."""
        return self.quantity * self.price_per_item

    def save(self, *args, **kwargs):
        """
        Custom save method to automatically fetch and store the price if it's not provided.
        IMPORTANT: You MUST implement the actual price fetching logic here based on your project's models.
        """
        if self.price_per_item is None and self.representation:
            # --- PRICE FETCHING LOGIC REQUIRED HERE ---
            # Example: If Representation has a method to get its current price:
            # self.price_per_item = self.representation.get_current_price()
            
            # Or, if prices are managed separately and linked to Representation:
            # Example: self.price_per_item = Price.objects.get(representation=self.representation).price
            
            # If price is essential and can't be auto-fetched reliably here,
            # consider making price_per_item non-nullable and requiring it during item creation.
            # For now, raising an error if price cannot be determined.
            raise ValueError("Price could not be determined for the cart item. Please ensure 'price_per_item' is set or implement price fetching logic in CartItem.save().")
            
        super().save(*args, **kwargs)
