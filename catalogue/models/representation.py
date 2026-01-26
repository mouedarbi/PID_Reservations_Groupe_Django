from django.db import models
from .show import *
from .location import *

# LE VRAI CODE EST EN COMMENTAIRE EN ATTENDANT QU'ON RECTIFIE LE NULL
"""
class RepresentationManager(models.Manager):
    def get_by_natural_key(self, show_slug, show_created_in, location_slug, location_website, schedule):
        show = Show.objects.get_by_natural_key(show_slug, show_created_in)
        location = Location.objects.get_by_natural_key(location_slug, location_website)
        return self.get(show_id=show.pk, location_id=location.pk, schedule=schedule)
"""
# Code temporaire qui gère si locality = null
class RepresentationManager(models.Manager):
    def get_by_natural_key(self, show_slug, show_created_in, location_slug, location_website, schedule):
        show = Show.objects.get_by_natural_key(show_slug, show_created_in)
        if location_slug is None and location_website is None:
            return self.get(show_id=show.pk, schedule=schedule, location__isnull=True)
        location = Location.objects.get_by_natural_key(location_slug, location_website)
        return self.get(show_id=show.pk, location_id=location.pk, schedule=schedule)
    
class Representation(models.Model):
    show = models.ForeignKey(Show, on_delete=models.RESTRICT, null=False, related_name='representations')
    schedule = models.DateTimeField()
    location = models.ForeignKey(Location, on_delete=models.RESTRICT, null=True, related_name='representations')
    available_seats = models.IntegerField(default=100)

    def __str__(self):
        return f"{self.show.slug} @ {self.schedule}"
    
    class Meta:
        db_table = "representations"

# C'est un code TEMPORAIRE
# il faudra d'abord régler la partie où locality_id : null dans la table locations

    def natural_key(self):
        if self.location_id:
            return (self.show.slug, self.show.created_in, 
                   self.location.slug, self.location.website, self.schedule)
        return (self.show.slug, self.show.created_in, None, None, self.schedule)
    
# Voici le code comment il doit être 
"""
    def natural_key(self):
        return (self.show.slug, self.show.created_in, 
                self.location.slug, self.location.website, self.schedule)
"""