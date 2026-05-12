from django.db import models

class GenreManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)

class Genre(models.Model):
    name = models.CharField(max_length=60, unique=True)
    
    # Les champs de traduction seront gérés par modeltranslation s'il est configuré,
    # mais nous les ajoutons ici explicitement pour être cohérents avec ton setup actuel.
    name_fr = models.CharField(max_length=60, null=True, blank=True)
    name_en = models.CharField(max_length=60, null=True, blank=True)
    name_nl = models.CharField(max_length=60, null=True, blank=True)

    objects = GenreManager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "genres"

    def natural_key(self):
        return (self.name,)
