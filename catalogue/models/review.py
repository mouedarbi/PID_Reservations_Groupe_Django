from django.db import models
from .show import *
from django.contrib.auth.models import User

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,
        null=True, related_name='user')
    show = models.ForeignKey(Show, on_delete=models.RESTRICT, 
		null=False, related_name='reviews')
    review = models.TextField()
    stars = models.PositiveSmallIntegerField()
    validated = models.BooleanField()
    is_pinned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)

    def __str__(self):
        username = self.user.username if self.user else "Utilisateur supprimé"
        return f"{username} - {self.show.title} : {self.stars}"
    
    class Meta:
        db_table = "reviews"