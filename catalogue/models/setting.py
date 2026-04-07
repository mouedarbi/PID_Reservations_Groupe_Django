from django.db import models

class AppSetting(models.Model):
    key = models.CharField(max_length=100, unique=True, verbose_name="Clé du paramètre")
    value = models.TextField(verbose_name="Valeur")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="Description")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.key

    @classmethod
    def get_value(cls, key, default=None):
        try:
            return cls.objects.get(key=key).value
        except cls.DoesNotExist:
            return default

    class Meta:
        db_table = "app_settings"
        verbose_name = "Paramètre de l'application"
        verbose_name_plural = "Paramètres de l'application"
