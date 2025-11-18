from django.db import models


class Locality(models.Model):
    locality = models.CharField(max_length=60)
    postcode = models.CharField(max_length=6)

    def __str__(self):
        return self.locality

    class Meta:
        db_table ="localities"