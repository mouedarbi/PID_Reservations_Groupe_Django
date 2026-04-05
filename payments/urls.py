from django.urls import path
from .views import CreateCheckoutSessionView, payment_success, payment_cancel

app_name = 'payments'

urlpatterns = [
    path('create-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('success/', payment_success, name='success'),
    path('cancel/', payment_cancel, name='cancel'),
]