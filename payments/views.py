import stripe
import os
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# On récupère la clé secrète depuis le .env que tu viens de remplir
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

class CreateCheckoutSessionView(APIView):
    def post(self, request):
        try:
            # Ici on crée la session Stripe
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'eur',
                            'product_data': {
                                'name': 'Réservation de matériel/salle',
                            },
                            'unit_amount': 2000, # Prix en centimes (ici 20,00 €)
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                # URL où l'utilisateur est renvoyé après le paiement
                success_url='http://127.0.0.1:8000/success/',
                cancel_url='http://127.0.0.1:8000/cancel/',
            )
            # On renvoie l'URL de la page de paiement Stripe au frontend
            return Response({'url': checkout_session.url})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)