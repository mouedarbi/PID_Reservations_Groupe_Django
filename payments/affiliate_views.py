import stripe
from django.conf import settings
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User
from catalogue.models import Affiliate, AffiliateTier, AffiliatePayment, AppSetting
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

class CreateAffiliateSessionView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('accounts:login')

        tier_id = request.POST.get('tier_id')
        tier = get_object_or_404(AffiliateTier, id=tier_id)

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

@csrf_exempt
def stripe_affiliate_webhook(request):
    """
    Webhook dédié uniquement à l'affiliation.
    """
    signature = request.META.get('HTTP_STRIPE_SIGNATURE')
    if not settings.STRIPE_WEBHOOK_SECRET:
        return HttpResponse(status=503)

    try:
        event = stripe.Webhook.construct_event(
            request.body,
            signature,
            settings.STRIPE_WEBHOOK_SECRET,
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    if event.get('type') == 'checkout.session.completed':
        session = event['data']['object']
        metadata = session.get('metadata', {})
        
        # On ne traite QUE si c'est un upgrade d'affiliation
        if 'tier_id' in metadata:
            tier_id = metadata.get('tier_id')
            user_id = metadata.get('user_id')
            if not tier_id or not user_id or session.get('payment_status') != 'paid':
                return HttpResponse(status=400)
            
            try:
                with transaction.atomic():
                    user = User.objects.get(id=user_id)
                    tier = AffiliateTier.objects.get(id=tier_id)
                    if session.get('amount_total') != int(tier.price * 100):
                        return HttpResponse(status=400)

                    affiliate, _ = Affiliate.objects.get_or_create(user=user)
                    affiliate.tier = tier
                    affiliate.save()

                    AffiliatePayment.objects.get_or_create(
                        stripe_session_id=session.get('id'),
                        defaults={
                            'affiliate': affiliate,
                            'stripe_payment_intent_id': session.get('payment_intent'),
                            'amount': (session.get('amount_total') or 0) / 100.0,
                            'currency': (session.get('currency') or 'EUR').upper(),
                        }
                    )
            except (User.DoesNotExist, AffiliateTier.DoesNotExist):
                return HttpResponse(status=400)

    return HttpResponse(status=200)

@login_required
def affiliate_success(request):
    session_id = request.GET.get('session_id')
    if not session_id:
        return redirect('accounts:user-api')

    stripe.api_key = AppSetting.get_value('STRIPE_SECRET_KEY')
    session = stripe.checkout.Session.retrieve(session_id)
    metadata = session.get('metadata', {})
    if (
        session.get('payment_status') != 'paid'
        or str(metadata.get('user_id')) != str(request.user.id)
        or not metadata.get('tier_id')
    ):
        return redirect('accounts:user-api')

    tier = get_object_or_404(AffiliateTier, id=metadata['tier_id'])
    if session.get('amount_total') != int(tier.price * 100):
        return redirect('accounts:user-api')

    with transaction.atomic():
        affiliate, _ = Affiliate.objects.get_or_create(user=request.user)
        affiliate.tier = tier
        affiliate.save(update_fields=['tier', 'updated_at'])
        AffiliatePayment.objects.get_or_create(
            stripe_session_id=session_id,
            defaults={
                'affiliate': affiliate,
                'stripe_payment_intent_id': session.get('payment_intent'),
                'amount': (session.get('amount_total') or 0) / 100.0,
                'currency': (session.get('currency') or 'EUR').upper(),
            }
        )

    return render(request, 'payments/success_api.html', {'tier': tier})
