from django.db import models
from .price import Price

class ShowPrice(models.Model):
    show = models.ForeignKey('Show', on_delete=models.CASCADE)
    price = models.ForeignKey(Price, on_delete=models.CASCADE)

    class Meta:
        db_table = "show_prices"
        unique_together = ('show', 'price')

    def __str__(self):
        return f"{self.show.title} - {self.price.type}"
