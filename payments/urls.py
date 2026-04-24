from django.urls import path
from .views import CreateCheckoutSessionView, CreateAffiliateSessionView, payment_success, payment_cancel, payment_failed

app_name = 'payments'

urlpatterns = [
    path('create-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('create-affiliate-session/', CreateAffiliateSessionView.as_view(), name='create-affiliate-session'),
    path('success/', payment_success, name='success'),
    path('cancel/', payment_cancel, name='cancel'),
    path('failed/', payment_failed, name='failed'),
]