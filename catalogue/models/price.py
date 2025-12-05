from django.db import models
import datetime

# Create your models here.
class Price(models.Model):
    type = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    
    def __str__(self):
        return f"{self.type} : {self.price} €"

    class Meta:
        db_table = "prices"
