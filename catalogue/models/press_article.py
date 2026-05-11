from django.db import models
from django.contrib.auth.models import User
from .show import Show

class PressArticle(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='press_articles')
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='press_articles')
    title = models.CharField(max_length=255)
    summary = models.TextField(max_length=500, help_text="Bref résumé de l'article pour l'affichage en liste.")
    content = models.TextField(help_text="Corps complet de l'article.")
    validated = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        username = self.user.username if self.user else "Auteur supprimé"
        return f"{self.title} - {username}"

    class Meta:
        db_table = "press_articles"
        verbose_name = "Article de Presse"
        verbose_name_plural = "Articles de Presse"
        ordering = ['-is_pinned', '-created_at']
