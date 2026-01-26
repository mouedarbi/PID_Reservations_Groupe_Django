from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from django.db import transaction

from catalogue.models import Representation, Reservation
from api.serializers.reservations import ReservationSerializer

class CheckoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """
        Processes the user's cart to create reservations.
        This transaction is atomic: all reservations are created or none are.
        """
        cart = request.session.get('cart', {})

        if not cart:
            return Response({"error": "Votre panier est vide."}, status=status.HTTP_400_BAD_REQUEST)

        created_reservations = []

        try:
            # First pass: Validate all items in cart before making changes
            for rep_id, item_data in cart.items():
                quantity = item_data.get('quantity')
                try:
                    representation = Representation.objects.get(pk=rep_id)
                    if representation.available_seats < quantity:
                        raise ValueError(f"Pas assez de places pour '{representation}'.")
                except Representation.DoesNotExist:
                    raise ValueError(f"La représentation avec l'ID {rep_id} n'existe pas.")

            # Second pass: Create reservations and update seats
            for rep_id, item_data in cart.items():
                quantity = item_data.get('quantity')
                representation = Representation.objects.get(pk=rep_id)
                
                # Create reservation
                reservation = Reservation.objects.create(
                    user=request.user,
                    representation=representation,
                    quantity=quantity,
                    status='Confirmed'
                )
                created_reservations.append(reservation)

                # Decrement available seats
                representation.available_seats -= quantity
                representation.save()
            
            # Clear the cart
            request.session['cart'] = {}

            # Serialize the created reservations to return them in the response
            serializer = ReservationSerializer(created_reservations, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            # This will catch validation errors from the first pass
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Generic error for any other issue
            return Response({"error": "Une erreur inattendue est survenue lors du paiement.", "detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)