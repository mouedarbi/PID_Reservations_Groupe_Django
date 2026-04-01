import stripe
import os
from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Configuration de la clé Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

class CreateCheckoutSessionView(APIView):
    def post(self, request):
        # 1. On récupère le panier (cart) depuis la session
        cart = request.session.get('cart', {})
        
        if not cart:
            return Response({'error': 'Votre panier est vide'}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Calcul du total du panier
        # Adapte 'price' et 'quantity' selon les noms dans ton application cart
        total_amount = 0
        for item in cart.values():
            total_amount += float(item['price']) * int(item['quantity'])

        try:
            # 3. Création de la session Stripe
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': 'Réservation d\'articles/salles',
                        },
                        'unit_amount': int(total_amount * 100), # Stripe veut des centimes (ex: 20€ = 2000)
                    },
                    'quantity': 1,
                }],
                mode='payment',
                # Les URLs de retour vers ton site
                success_url='http://127.0.0.1:8000/payments/success/',
                cancel_url='http://127.0.0.1:8000/payments/cancel/',
            )
            return Response({'url': checkout_session.url})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Vues pour les pages de confirmation (HTML)
def payment_success(request):
    # On vide le panier une fois payé
    if 'cart' in request.session:
        del request.session['cart']
    return render(request, 'payments/success.html')

def payment_cancel(request):
    return render(request, 'payments/cancel.html')