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
from django.contrib import messages
from django.shortcuts import redirect
from django.views import View
from catalogue.models import AffiliateTier, Affiliate


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


class CreateAffiliateSessionView(View):
    """
    Gère la création d'une session Stripe pour l'achat d'un plan d'affiliation.
    """
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('accounts:login')

        tier_id = request.POST.get('tier_id')
        try:
            tier = AffiliateTier.objects.get(id=tier_id)
        except AffiliateTier.DoesNotExist:
            messages.error(request, "Plan d'affiliation introuvable.")
            return redirect('accounts:user-api')

        # Si le plan est gratuit (Free), on change juste le plan sans passer par Stripe
        if tier.price <= 0:
            affiliate, created = Affiliate.objects.get_or_create(user=request.user)
            affiliate.tier = tier
            affiliate.save()
            messages.success(request, f"Votre plan a été mis à jour vers : {tier.name}")
            return redirect('accounts:user-api')

        # Configuration Stripe
        stripe.api_key = AppSetting.get_value('STRIPE_SECRET_KEY')
        base_url = f"{request.scheme}://{request.get_host()}"

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card', 'bancontact', 'sepa_debit'],
                line_items=[{
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': f"Abonnement API - {tier.name}",
                            'description': f"Accès API ThéâtrePlus (Limite: {tier.api_limit_daily} appels/jour)",
                        },
                        'unit_amount': int(tier.price * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                metadata={
                    'payment_type': 'affiliation_upgrade',
                    'user_id': request.user.id,
                    'tier_id': tier.id
                },
                success_url=base_url + reverse('payments:success') + "?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=base_url + reverse('accounts:user-api'),
            )
            return redirect(checkout_session.url, status=303)
        except Exception as e:
            messages.error(request, f"Erreur Stripe : {str(e)}")
            return redirect('accounts:user-api')


from catalogue.models.reservation import Reservation, RepresentationReservation
from catalogue.models.representation import Representation
from catalogue.models.price import Price
from catalogue.models.ticket import Ticket
from catalogue.views.ticket import send_reservation_email
from .models import Payment

# Vues pour les pages de confirmation (HTML)
def payment_success(request):
    # On initialise le panier
    cart = Cart(request)
    
    # On récupère l'ID de session Stripe
    session_id = request.GET.get('session_id')
    
    # On vérifie que l'ID de session est présent
    if session_id:
        try:
            # On vérifie si ce paiement n'a pas déjà été traité pour éviter les doublons
            if not Payment.objects.filter(stripe_session_id=session_id).exists():
                # On récupère les détails de la session depuis Stripe
                stripe.api_key = AppSetting.get_value('STRIPE_SECRET_KEY')
                session = stripe.checkout.Session.retrieve(session_id)
                
                # RÉCUPÉRATION DES MÉTADONNÉES
                metadata = session.metadata
                payment_type = metadata.get('payment_type', 'ticket_reservation')

                # CAS 1 : UPGRADE AFFILIATION
                if payment_type == 'affiliation_upgrade':
                    user_id = metadata.get('user_id')
                    tier_id = metadata.get('tier_id')
                    
                    user = User.objects.get(id=user_id)
                    tier = AffiliateTier.objects.get(id=tier_id)
                    
                    affiliate, created = Affiliate.objects.get_or_create(user=user)
                    affiliate.tier = tier
                    affiliate.save()
                    
                    # On crée quand même une trace de paiement (optionnel mais recommandé)
                    Payment.objects.create(
                        stripe_session_id=session_id,
                        stripe_payment_intent_id=session.payment_intent,
                        amount=session.amount_total / 100.0,
                        currency=session.currency.upper(),
                        status="succeeded"
                    )
                    
                    messages.success(request, f"Félicitations ! Votre accès API est maintenant en mode {tier.name}.")
                    return render(request, 'payments/success_api.html', {'tier': tier})

                # CAS 2 : RÉSERVATION DE TICKETS (Comportement original)
                elif request.user.is_authenticated and len(cart) > 0:
                    # 1. Création de la réservation parente
                    reservation = Reservation.objects.create(
                        user=request.user,
                        status="paid"
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
                        representation = item['representation']
                        requested_quantity = item['quantity']
                        
                        rep_res = RepresentationReservation.objects.create(
                            reservation=reservation,
                            representation=representation,
                            price=item['price_obj'],
                            quantity=requested_quantity
                        )
                        
                        for _ in range(requested_quantity):
                            Ticket.objects.create(representation_reservation=rep_res)

                        representation.available_seats -= requested_quantity
                        representation.save()
                        
                    cart.clear()
                    send_reservation_email(reservation)
        except Exception as e:
            print(f"Erreur lors de la validation du paiement: {e}")
            return render(request, 'payments/failed.html', {'error': str(e)})
        
    return render(request, 'payments/success.html')

def payment_cancel(request):
    return render(request, 'payments/cancel.html')

def payment_failed(request):
    return render(request, 'payments/failed.html')
