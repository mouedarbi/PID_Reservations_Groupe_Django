import stripe
import os
from django.conf import settings
from django.shortcuts import render
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from cart.cart import Cart  # Utiliser la classe Cart existante

# Configuration de la clé Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

class CreateCheckoutSessionView(APIView):
    def post(self, request):
        # 1. On initialise le panier via la classe Cart
        cart = Cart(request)
        
        if len(cart) == 0:
            return Response({'error': 'Votre panier est vide'}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Récupérer le total du panier
        total_amount = cart.get_total_price()

        try:
            # Construction de l'URL de base pour les retours
            base_url = f"{request.scheme}://{request.get_host()}"

            # 3. Création de la session Stripe
            # On ajoute 'bancontact' et 'sepa_debit' pour le paiement sans carte (en ligne)
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card', 'bancontact', 'sepa_debit'],
                line_items=[{
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': 'Réservation de places de spectacle - ThéâtrePlus',
                        },
                        'unit_amount': int(total_amount * 100), # Stripe veut des centimes
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=base_url + reverse('payments:success'),
                cancel_url=base_url + reverse('payments:cancel'),
            )
            return Response({'url': checkout_session.url})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Vues pour les pages de confirmation (HTML)
def payment_success(request):
    # On vide le panier une fois payé
    cart = Cart(request)
    cart.clear()
    return render(request, 'payments/success.html')

def payment_cancel(request):
    return render(request, 'payments/cancel.html')