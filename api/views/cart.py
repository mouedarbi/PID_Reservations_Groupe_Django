from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from django.db import transaction # For atomic operations
from django.http import Http404
import decimal # Added for placeholder price

# Corrected import for Cart and CartItem models
from catalogue.models.cart import Cart, CartItem
# Assuming Representation model exists in catalogue app
from catalogue.models.representation import Representation
# Corrected import for serializers
from api.serializers.cart import CartSerializer, CartItemSerializer


class CartView(APIView):
    """
    Retrieve the authenticated user's cart, or create one if it doesn't exist.
    GET /api/cart/
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartItemAddUpdateView(APIView):
    """
    Add a new item to the authenticated user's cart or update its quantity.
    Expects {"representation_id": <int>, "quantity": <int>} in request.data.
    POST /api/cart/items/
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        user = request.user
        representation_id = request.data.get('representation_id')
        quantity_to_add = request.data.get('quantity', 1) # Default to 1 if not provided

        # --- Basic input validation ---
        if not representation_id or not isinstance(quantity_to_add, int) or quantity_to_add <= 0:
            return Response({"detail": "Invalid representation_id or quantity."}, status=status.HTTP_400_BAD_REQUEST)

        # --- Fetch Representation ---
        try:
            representation = Representation.objects.get(id=representation_id)
        except Representation.DoesNotExist:
            return Response({"detail": "Representation not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # --- Placeholder Price Logic ---
        # This is a temporary fix. You MUST replace this with your actual price logic.
        price_per_item = decimal.Decimal('25.00') 

        # --- Get or Create User's Cart ---
        cart, _ = Cart.objects.get_or_create(user=user)

        with transaction.atomic(): # Ensure database operations are atomic
            # --- Get or Create CartItem and Update Quantity ---
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                representation=representation,
                defaults={'quantity': 0, 'price_per_item': price_per_item} # Set default price for new items
            )

            # Calculate new total quantity after adding
            new_total_quantity = cart_item.quantity + quantity_to_add
            
            # --- Inventory Check ---
            # Assuming Representation model has 'available_seats'
            if not hasattr(representation, 'available_seats'):
                return Response({"detail": "Representation model is missing 'available_seats' attribute."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            if new_total_quantity > representation.available_seats:
                return Response(
                    {"detail": f"Not enough seats available. Max {representation.available_seats} for this representation."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Update existing cart item
            cart_item.quantity = new_total_quantity
            # Ensure price is current if needed, or stick to initial price if business logic dictates
            cart_item.price_per_item = price_per_item 
            cart_item.save()

            # --- Return updated cart ---
            serializer = CartSerializer(cart)
            return Response(serializer.data, status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED)


class CartItemDetailView(APIView):
    """
    Retrieve, Update, or Delete a specific cart item belonging to the authenticated user's cart.
    GET /api/cart/items/<int:pk>/
    PATCH /api/cart/items/<int:pk>/
    DELETE /api/cart/items/<int:pk>/
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, user):
        """Helper method to get a CartItem by pk, ensuring it belongs to the user."""
        try:
            return CartItem.objects.get(pk=pk, cart__user=user)
        except CartItem.DoesNotExist:
            raise Http404 # Raise Http404 directly

    def get(self, request, pk, format=None):
        item = self.get_object(pk, request.user)
        serializer = CartItemSerializer(item)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        item = self.get_object(pk, request.user)
        
        # --- Inventory Check for quantity update ---
        quantity_data = request.data.get('quantity')
        if quantity_data is not None:
            if not isinstance(quantity_data, int) or quantity_data <= 0:
                return Response({"detail": "Quantity must be a positive integer."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Assuming Representation has 'available_seats'
            if not hasattr(item.representation, 'available_seats'):
                return Response({"detail": "Representation model is missing 'available_seats' attribute."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            if quantity_data > item.representation.available_seats:
                return Response(
                    {"detail": f"Only {item.representation.available_seats} seats available for this representation."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # --- Update CartItem ---
        serializer = CartItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            # Return the whole cart for updated totals in the response
            return Response(CartSerializer(item.cart).data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        item = self.get_object(pk, request.user)
        item.delete()
        # Return the whole cart for updated totals in the response
        return Response(CartSerializer(item.cart).data, status=status.HTTP_200_OK)


class CartClearView(APIView):
    """
    Clear all items from the authenticated user's cart.
    DELETE /api/cart/clear/
    """
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, format=None):
        cart = get_object_or_404(Cart, user=request.user)
        cart.items.all().delete()
        # Return empty cart or success message
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)