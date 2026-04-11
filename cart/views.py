import stripe
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .cart import Cart  # Assure-toi que le fichier cart.py est bien dans le même dossier
from catalogue.models import Representation, Price, Reservation, RepresentationReservation
stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def cart_checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.error(request, "Votre panier est vide.")
        return redirect('catalogue:show-index')

    if request.method == 'POST':
        # 1. Préparation des articles pour Stripe
        line_items = []
        for item in cart:
            line_items.append({
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': item['representation'].show.title,
                    },
                    'unit_amount': int(item['price_obj'].price * 100), # Stripe veut des centimes
                },
                'quantity': item['quantity'],
            })

        try:
            # 2. Création de la session Stripe
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card', 'bancontact', 'sepa_debit'],
                line_items=line_items,
                mode='payment',
                # URLs vers lesquelles Stripe renvoie l'utilisateur
                success_url=request.build_absolute_uri(reverse('payments:success')),
                cancel_url=request.build_absolute_uri(reverse('payments:cancel')),
            )
            
            # 3. REDIRECTION DIRECTE VERS STRIPE
            return redirect(checkout_session.url, code=303)

        except Exception as e:
            messages.error(request, f"Erreur Stripe : {str(e)}")
            return redirect('cart:cart_detail')

    return render(request, 'cart/checkout.html', {'cart': cart})