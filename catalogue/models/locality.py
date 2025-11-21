from django.db import models


class Locality(models.Model):
    locality = models.CharField(max_length=60)
    postal_code = models.CharField(max_length=6)

    def __str__(self):
        return f"{self.postal_code} {self.locality}"

    class Meta:
        db_table ="localities"