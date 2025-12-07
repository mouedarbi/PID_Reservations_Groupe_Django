from django.db import models
from django.contrib.auth.models import User


class Reservation(models.Model):
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=60)
    user = models.ForeignKey(User, on_delete=models.RESTRICT,
                             null=False, related_name='reservations')

    def __str__(self):
        return f"{self.user} - {self.booking_date}"

    class Meta:
        db_table = "reservations"
