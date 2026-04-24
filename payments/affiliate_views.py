import stripe
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User
from catalogue.models import Affiliate, AffiliateTier, AffiliatePayment, AppSetting
from django.contrib.auth.decorators import login_required

class CreateAffiliateSessionView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('accounts:login')

        tier_id = request.POST.get('tier_id')
        tier = AffiliateTier.objects.get(id=tier_id)

        if tier.price <= 0:
            affiliate, _ = Affiliate.objects.get_or_create(user=request.user)
            affiliate.tier = tier
            affiliate.save()
            return redirect('accounts:user-api')

        stripe.api_key = AppSetting.get_value('STRIPE_SECRET_KEY')
        base_url = f"{request.scheme}://{request.get_host()}"

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {'name': f"API {tier.name}"},
                    'unit_amount': int(tier.price * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            metadata={'tier_id': tier.id, 'user_id': request.user.id},
            success_url=base_url + reverse('payments:affiliate_success') + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=base_url + reverse('accounts:user-api'),
        )
        return redirect(checkout_session.url, status=303)

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json

@csrf_exempt
def stripe_affiliate_webhook(request):
    """
    Webhook dédié uniquement à l'affiliation.
    """
    payload = request.body
    try:
        event = json.loads(payload)
    except Exception:
        return HttpResponse(status=400)

    if event.get('type') == 'checkout.session.completed':
        session = event['data']['object']
        metadata = session.get('metadata', {})
        
        # On ne traite QUE si c'est un upgrade d'affiliation
        if 'tier_id' in metadata:
            tier_id = metadata['tier_id']
            user_id = metadata['user_id']
            
            try:
                user = User.objects.get(id=user_id)
                tier = AffiliateTier.objects.get(id=tier_id)
                
                affiliate, _ = Affiliate.objects.get_or_create(user=user)
                affiliate.tier = tier
                affiliate.save()
                
                # Trace du paiement dans AffiliatePayment
                AffiliatePayment.objects.get_or_create(
                    stripe_session_id=session.get('id'),
                    defaults={
                        'affiliate': affiliate,
                        'stripe_payment_intent_id': session.get('payment_intent'),
                        'amount': session.get('amount_total', 0) / 100.0,
                        'currency': session.get('currency', 'EUR').upper(),
                    }
                )
                print(f"WEBHOOK SUCCESS: Plan {tier.name} activé pour {user.username}")
            except Exception as e:
                print(f"WEBHOOK ERROR: {str(e)}")

    return HttpResponse(status=200)

@login_required
def affiliate_success(request):
    session_id = request.GET.get('session_id')
    stripe.api_key = AppSetting.get_value('STRIPE_SECRET_KEY')
    session = stripe.checkout.Session.retrieve(session_id)
    
    tier_id = session.metadata.tier_id
    tier = AffiliateTier.objects.get(id=tier_id)
    
    affiliate, _ = Affiliate.objects.get_or_create(user=request.user)
    affiliate.tier = tier
    affiliate.save()

    # On enregistre dans NOTRE nouveau modèle séparé
    AffiliatePayment.objects.get_or_create(
        stripe_session_id=session_id,
        defaults={
            'affiliate': affiliate,
            'stripe_payment_intent_id': session.payment_intent,
            'amount': session.amount_total / 100.0,
            'currency': session.currency.upper(),
        }
    )

    return render(request, 'payments/success_api.html', {'tier': tier})
