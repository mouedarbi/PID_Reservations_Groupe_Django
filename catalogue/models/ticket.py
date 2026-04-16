import uuid
from django.db import models
from .reservation import RepresentationReservation

class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    representation_reservation = models.ForeignKey(
        RepresentationReservation, 
        on_delete=models.CASCADE, 
        related_name='tickets'
    )
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket {self.id} - {self.representation_reservation.representation.show.title}"

    class Meta:
        db_table = "tickets"
        verbose_name = "Billet"
        verbose_name_plural = "Billets"
