from django.db import models
from .show import Show
from .price import Price

class PriceShow(models.Model):
    show = models.ForeignKey(
        Show,
        on_delete=models.RESTRICT,
        null=False,
        related_name="price_links",
    )
    price = models.ForeignKey(
        Price,
        on_delete=models.RESTRICT,
        null=False,
        related_name="show_links",
    )

    def __str__(self):
        return f"{self.show.title} - {self.price.type}"

    class Meta:
        db_table = "price_show"
        unique_together = ("show", "price")
