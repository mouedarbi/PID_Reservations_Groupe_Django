from django.db import models
from .show import *
from .location import *

class Representation(models.Model):
    show = models.ForeignKey(Show, on_delete=models.RESTRICT, null=False, related_name='representations')
    schedule = models.DateTimeField()
    location = models.ForeignKey(Location, on_delete=models.RESTRICT, null=True, related_name='representations')

    def __str__(self):
        return f"{self.show.slug} @ {self.schedule}"
    
    class Meta:
        db_table = "representations"
