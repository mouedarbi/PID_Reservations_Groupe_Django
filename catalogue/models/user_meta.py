from django.db import models
from django.contrib.auth.models import User

class UserMeta(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    langue = models.CharField(max_length=2)

    def __str__(self):
        return self.user.first_name +" "+ self.user.last_name

    class Meta:
        db_table = "user_meta"
