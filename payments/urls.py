from django.urls import path
from .views import CreateCheckoutSessionView, payment_success, payment_cancel, payment_failed
from .affiliate_views import CreateAffiliateSessionView, affiliate_success, stripe_affiliate_webhook

app_name = 'payments'

urlpatterns = [
    path('create-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('create-affiliate-session/', CreateAffiliateSessionView.as_view(), name='affiliate-create-session'),
    path('success/', payment_success, name='success'),
    path('affiliate-success/', affiliate_success, name='affiliate_success'),
    path('webhook/', stripe_affiliate_webhook, name='stripe-webhook'),
    path('cancel/', payment_cancel, name='cancel'),
    path('failed/', payment_failed, name='failed'),
]