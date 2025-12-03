from django.db import models

class PriceManager(models.Manager):
    def get_by_natural_key(self, type):
        return self.get(type=type)

class Price(models.Model):
    type = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()

    objects = PriceManager()

    def __str__(self):
        return f"{self.type} : {self.price} €"

    class Meta:
        db_table = "prices"
        constraints = [
            models.UniqueConstraint(
                fields=["type"],
                name="unique_price_type",
            ),
        ]

    def natural_key(self):
        return (self.type,)

