from django.db import models


class Price(models.Model):

    type = models.CharField(max_length=30)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    description = models.CharField(max_length=120)
    start_date = models.DateField()
    end_date = models.DateField()


    def __str__(self):
        return self.price

    class Meta:
        db_table = "prices"