from django.db import models


class LocalityManager(models.Manager):
    def get_by_natural_key(self, postal_code, locality):
        return self.get(postal_code=postal_code, locality=locality)


class Locality(models.Model):
    postal_code = models.CharField(max_length=6)
    locality = models.CharField(max_length=30)

    objects = LocalityManager()

    def __str__(self):
        return f"{self.postal_code} {self.locality}"

    class Meta:
        db_table = "localities"
        constraints = [
            models.UniqueConstraint(
                fields=["postal_code", "locality"],
                name="unique_postal_code_locality",
            ),
        ]

    def natural_key(self):
        return (self.postal_code, self.locality)
