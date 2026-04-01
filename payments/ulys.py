from django.urls import path
from .views import CreateCheckoutSessionView

urlpatterns = [
    path('create-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
]