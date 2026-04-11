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

from django.shortcuts import redirect
from django.views import View

class CreateCheckoutSessionView(View):
    def post(self, request):
        # 1. On initialise le panier via la classe Cart
        cart = Cart(request)
        
        if len(cart) == 0:
            # Redirection vers le panier avec un message d'erreur si possible
            return redirect('cart:cart_detail')

        # 2. Récupérer le total du panier
        total_amount = cart.get_total_price()

        try:
            # Construction de l'URL de base pour les retours
            base_url = f"{request.scheme}://{request.get_host()}"

            # 3. Création de la session Stripe
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
            # REDIRECTION DIRECTE (100% Python)
            return redirect(checkout_session.url, status=303)
            
        except Exception as e:
            # En cas d'erreur, on revient au panier
            return redirect('cart:cart_detail')

from catalogue.models.reservation import Reservation, RepresentationReservation
from catalogue.models.representation import Representation
from catalogue.models.price import Price

# Vues pour les pages de confirmation (HTML)
def payment_success(request):
    # On initialise le panier
    cart = Cart(request)
    
    # On vérifie que l'utilisateur est connecté et que le panier n'est pas vide
    if request.user.is_authenticated and len(cart) > 0:
        # 1. Création de la réservation parente
        reservation = Reservation.objects.create(
            user=request.user,
            status="paid"  # Statut de la réservation
        )
        
        # 2. Création du détail pour chaque article du panier
        for item in cart:
            RepresentationReservation.objects.create(
                reservation=reservation,
                representation=item['representation'],
                price=item['price_obj'],
                quantity=item['quantity']
            )
            
        # 3. On vide le panier une fois payé et enregistré
        cart.clear()
        
    return render(request, 'payments/success.html')

def payment_cancel(request):
    return render(request, 'payments/cancel.html')