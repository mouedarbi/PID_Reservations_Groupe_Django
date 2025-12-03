from django.db import models
from .show import *
from .artist_type import *

class ArtistTypeShow(models.Model):
    show = models.ForeignKey(
        Show,
        on_delete=models.CASCADE,
        null=False,
        related_name='artistTypeShows'
    )
    artist_type = models.ForeignKey(
        ArtistType,
        on_delete=models.CASCADE,
        null=False,
        related_name='artistTypeShows'
    )

    class Meta:
        unique_together = ("show", "artist_type")  # Optional constraint
        db_table = "artist_type_show"
