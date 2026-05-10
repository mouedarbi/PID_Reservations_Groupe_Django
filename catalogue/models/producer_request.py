from django.db import models
from django.contrib.auth.models import User

class ProducerRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('approved', 'Approuvé'),
        ('rejected', 'Refusé'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='producer_requests')
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    address = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=30)
    presentation = models.TextField(max_length=500)
    motivation = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Demande de {self.first_name} {self.last_name} ({self.user.username})"

    class Meta:
        db_table = "producer_requests"
        verbose_name = "Demande Producteur"
        verbose_name_plural = "Demandes Producteurs"
