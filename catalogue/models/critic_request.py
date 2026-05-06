from django.db import models
from django.contrib.auth.models import User

class CriticRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('approved', 'Approuvé'),
        ('rejected', 'Refusé'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='critic_requests')
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    profession = models.CharField(max_length=100)
    media_name = models.CharField(max_length=100)
    website = models.URLField(max_length=255, null=True, blank=True)
    motivation = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Demande Critique de {self.first_name} {self.last_name} ({self.user.username})"

    class Meta:
        db_table = "critic_requests"
        verbose_name = "Demande Critique"
        verbose_name_plural = "Demandes Critiques"
