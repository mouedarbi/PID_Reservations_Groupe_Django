from django.db import models

class ArtistManager(models.Manager):
    def get_by_natural_key(self, firstname, lastname):
        return self.get(firstname=firstname, lastname=lastname)

class Artist(models.Model):
    firstname = models.CharField(max_length=60)
    lastname = models.CharField(max_length=60)

    objects = ArtistManager()

    def __str__(self):
        return self.firstname +" "+self.lastname
    
    class Meta:
        db_table = "artists"
        constraints = [
            models.UniqueConstraint(
                fields=["firstname", "lastname"],
                name="unique_firstname_lastname",
            ),
        ]

    def natural_key(self):
        return (self.firstname, self.lastname)