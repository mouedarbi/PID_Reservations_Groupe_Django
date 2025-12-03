from django.db import models
from .show import *
from django.contrib.auth.models import User

class Review(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        null=False,
        related_name='reviews'
    )
    show = models.ForeignKey(
        Show,
        on_delete=models.RESTRICT,
        null=False,
        related_name='reviews'
    )
    review = models.TextField()
    stars = models.PositiveSmallIntegerField()
    validated = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.user.username} - {self.show.title} : {self.stars}"

    class Meta:
        db_table = "reviews"
