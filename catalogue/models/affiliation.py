from django.db import models
from django.contrib.auth.models import User
import uuid

class AffiliateTier(models.Model):
    """
    Représente les différents niveaux d'affiliation (Free, Starter, Premium).
    """
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stripe_price_id = models.CharField(max_length=100, blank=True, null=True, help_text="ID du prix Stripe pour l'abonnement")
    api_limit_daily = models.IntegerField(default=100, help_text="Nombre maximum d'appels API autorisés par jour")
    can_access_full_data = models.BooleanField(default=False, help_text="Si activé, donne accès aux détails complets (artistes, prix, etc.)")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Niveau d'affiliation"
        verbose_name_plural = "Niveaux d'affiliation"

class Affiliate(models.Model):
    """
    Profil d'affilié lié à un utilisateur Django.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='affiliate_profile')
    tier = models.ForeignKey(AffiliateTier, on_delete=models.SET_NULL, null=True, blank=True)
    api_key = models.CharField(max_length=100, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Génération d'une clé API unique si elle n'existe pas
        if not self.api_key:
            self.api_key = str(uuid.uuid4()).replace('-', '')
        super().save(*args, **kwargs)

    def __str__(self):
        tier_name = self.tier.name if self.tier else "Aucun"
        return f"{self.user.username} - {tier_name}"

    class Meta:
        verbose_name = "Affilié"
        verbose_name_plural = "Affiliés"
