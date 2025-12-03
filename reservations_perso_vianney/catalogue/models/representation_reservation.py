from django.db import models
from .representation import Representation
from .reservation import Reservation

class RepresentationReservation(models.Model):
    representation = models.ForeignKey(
        Representation,
        on_delete=models.RESTRICT,
        null=False,
        related_name="representation_reservations",
    )
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.RESTRICT,
        null=False,
        related_name="representation_reservations",
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.reservation.user} - {self.representation} ({self.quantity} x {self.price} €)"

    class Meta:
        db_table = "representation_reservation"
        unique_together = ("representation", "reservation")
