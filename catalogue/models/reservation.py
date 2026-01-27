from django.db import models
from django.contrib.auth.models import User
from .representation import Representation
from .price import Price


class Reservation(models.Model):
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=60)
    user = models.ForeignKey(User, on_delete=models.RESTRICT,
                             null=False, related_name='reservations')
    
    representations = models.ManyToManyField(Representation, through='RepresentationReservation')

    def __str__(self):
        return f"{self.user} - {self.booking_date}"

    class Meta:
        db_table = "reservations"


class RepresentationReservation(models.Model):
    representation = models.ForeignKey(Representation, on_delete=models.RESTRICT)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='representation_reservations')
    price = models.ForeignKey(Price, on_delete=models.RESTRICT)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = "representation_reservation"