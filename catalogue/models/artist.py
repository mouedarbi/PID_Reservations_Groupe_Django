from django.db import models

<<<<<<< HEAD
#create your modele here

class Artist(models.Model):
    firstname = models.CharField(max_length = 60)
    lastname = models.CharField(max_length=60)
    
=======
class ArtistManager(models.Manager):
    def get_by_natural_key(self, firstname, lastname):
        return self.get(firstname=firstname, lastname=lastname)

class Artist(models.Model):
    firstname = models.CharField(max_length=60)
    lastname = models.CharField(max_length=60)

    objects = ArtistManager()

>>>>>>> c9ae4db4ee72dcad93f88e8a92c3e9a936cc3925
    def __str__(self):
        return self.firstname +" "+self.lastname
    
    class Meta:
<<<<<<< HEAD
        db_table = "artists"
=======
        db_table = "artists"
        constraints = [
            models.UniqueConstraint(
                fields=["firstname", "lastname"],
                name="unique_firstname_lastname",
            ),
        ]

    def natural_key(self):
        return (self.firstname, self.lastname)
>>>>>>> c9ae4db4ee72dcad93f88e8a92c3e9a936cc3925
