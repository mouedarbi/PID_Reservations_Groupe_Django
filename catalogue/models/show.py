from django.db import models
from .location import *



class Show(models.Model):
    slug = models.CharField(max_length=60, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255, null=True)
    poster_url = models.CharField(max_length=255, null=True)
    duration = models.PositiveSmallIntegerField(null=True)
    created_in = models.DateField(auto_now_add=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='shows')
    bookable = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "shows"

