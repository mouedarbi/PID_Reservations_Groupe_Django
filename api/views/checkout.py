from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from django.db import transaction

from catalogue.models import Price, Representation, RepresentationReservation, Reservation
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

        try:
            reservation = Reservation.objects.create(
                user=request.user,
                status='PAID',
            )

            for item_data in cart.values():
                representation_id = item_data.get('representation_id')
                price_id = item_data.get('price_id')
                quantity = item_data.get('quantity')
                representation = Representation.objects.select_for_update().get(
                    pk=representation_id
                )
                price = Price.objects.get(pk=price_id)
                if quantity is None or quantity < 1:
                    raise ValueError('La quantité doit être supérieure à zéro.')
                if not representation.show.prices.filter(pk=price.pk).exists():
                    raise ValueError('Le tarif ne correspond pas au spectacle.')
                if representation.available_seats < quantity:
                    raise ValueError(f"Pas assez de places pour '{representation}'.")

                RepresentationReservation.objects.create(
                    reservation=reservation,
                    representation=representation,
                    price=price,
                    quantity=quantity,
                )
                representation.available_seats -= quantity
                representation.save(update_fields=['available_seats'])
            
            request.session['cart'] = {}
            serializer = ReservationSerializer(reservation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            # This will catch validation errors from the first pass
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (Price.DoesNotExist, Representation.DoesNotExist):
            return Response(
                {"error": "Un article du panier n'existe plus."},
                status=status.HTTP_400_BAD_REQUEST,
            )