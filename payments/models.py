from django.db import models
from catalogue.models.reservation import Reservation

class Payment(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='payment', null=True, blank=True)
    stripe_session_id = models.CharField(max_length=255, unique=True, verbose_name="ID de session Stripe")
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, null=True, verbose_name="ID de paiement Stripe")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant payé")
    currency = models.CharField(max_length=3, default='EUR', verbose_name="Devise")
    status = models.CharField(max_length=20, default='pending', verbose_name="Statut du paiement")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de transaction")

    def __str__(self):
        return f"Paiement {self.stripe_session_id} - {self.amount} {self.currency}"

    class Meta:
        verbose_name = "Paiement"
        verbose_name_plural = "Paiements"
