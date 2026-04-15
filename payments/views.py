import stripe
import os
from django.conf import settings
from django.shortcuts import render
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from cart.cart import Cart  # Utiliser la classe Cart existante
from catalogue.models.setting import AppSetting

from django.shortcuts import redirect
from django.views import View

class CreateCheckoutSessionView(View):
    def post(self, request):
        # Configuration dynamique de la clé Stripe depuis la DB
        stripe.api_key = AppSetting.get_value('STRIPE_SECRET_KEY')
        
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
                success_url=base_url + reverse('payments:success') + "?session_id={CHECKOUT_SESSION_ID}",
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
from .models import Payment

# Vues pour les pages de confirmation (HTML)
def payment_success(request):
    # On initialise le panier
    cart = Cart(request)
    
    # On récupère l'ID de session Stripe
    session_id = request.GET.get('session_id')
    
    # On vérifie que l'utilisateur est connecté et que le panier n'est pas vide
    if request.user.is_authenticated and len(cart) > 0 and session_id:
        try:
            # On vérifie si ce paiement n'a pas déjà été traité pour éviter les doublons
            if not Payment.objects.filter(stripe_session_id=session_id).exists():
                # On récupère les détails de la session depuis Stripe
                stripe.api_key = AppSetting.get_value('STRIPE_SECRET_KEY')
                session = stripe.checkout.Session.retrieve(session_id)
                
                # 1. Création de la réservation parente
                reservation = Reservation.objects.create(
                    user=request.user,
                    status="paid"  # Statut de la réservation
                )
                
                # 2. Création de la trace du paiement
                Payment.objects.create(
                    reservation=reservation,
                    stripe_session_id=session_id,
                    stripe_payment_intent_id=session.payment_intent,
                    amount=session.amount_total / 100.0,
                    currency=session.currency.upper(),
                    status="succeeded"
                )
                
                # 3. Création du détail pour chaque article du panier
                for item in cart:
                    RepresentationReservation.objects.create(
                        reservation=reservation,
                        representation=item['representation'],
                        price=item['price_obj'],
                        quantity=item['quantity']
                    )
                    
                    # MISE À JOUR DU STOCK (Places disponibles)
                    representation = item['representation']
                    if representation.available_seats:
                        representation.available_seats -= item['quantity']
                        representation.save()
                    
                # 4. On vide le panier une fois payé et enregistré
                cart.clear()
        except Exception as e:
            # En cas d'erreur lors du traitement de la session Stripe
            print(f"Erreur lors de la validation du paiement: {e}")
            return render(request, 'payments/failed.html', {'error': str(e)})
        
    return render(request, 'payments/success.html')

def payment_cancel(request):
    return render(request, 'payments/cancel.html')

def payment_failed(request):
    return render(request, 'payments/failed.html')