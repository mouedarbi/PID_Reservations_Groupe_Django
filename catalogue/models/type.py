from django.db import models

# Create your models here.
class Type(models.Model):
    type = models.CharField(max_length=60)

    def __str__(self):
        return self.type
    
    class Meta:
        db_table = "types"