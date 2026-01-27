from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from catalogue.models import UserMeta

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Créer UserMeta automatiquement
        UserMeta.objects.get_or_create(user=instance, defaults={'langue': 'fr'})
        
        # Ajouter au groupe MEMBER par défaut
        try:
            group = Group.objects.get(name='MEMBER')
            instance.groups.add(group)
        except Group.DoesNotExist:
            pass
