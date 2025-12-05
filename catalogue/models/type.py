from django.db import models

class TypeManager(models.Manager):
    def get_by_natural_key(self, type,):
        return self.get(type=type,)

class Type(models.Model):
    type =  models.CharField(max_length=60)

    objects = TypeManager()

    def __str__(self):
        return self.type

    class Meta:
        db_table = "types"

    def natural_key(self):
        return (self.type,)