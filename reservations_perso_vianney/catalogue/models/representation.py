from django.db import models
from .show import Show
from .location import Location
from .reservation import Reservation

class Representation(models.Model):
    schedule = models.DateTimeField()
    show = models.ForeignKey(Show, on_delete=models.RESTRICT, related_name='representations')
    location = models.ForeignKey(Location, on_delete=models.RESTRICT, null=True, related_name='representations')

    # ManyToMany logique via le modèle pivot
    reservations = models.ManyToManyField(
        Reservation,
        through="RepresentationReservation",
        related_name="representations",
    )

    def __str__(self):
        return f"{self.show.title} @ {self.schedule}"

    class Meta:
        db_table = "representations"
