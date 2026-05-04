from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from catalogue.models import ProducerRequest, Show, Notification
from django.urls import reverse

@receiver(post_save, sender=User)
def notify_new_user(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            type='new_user',
            title='Nouvel Utilisateur',
            message=f"✨ <b>{instance.username}</b> vient de rejoindre ThéâtrePlus ! Bienvenue à notre nouveau membre.",
            link=reverse('admin_user_index')
        )

@receiver(post_save, sender=ProducerRequest)
def notify_producer_request(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            type='producer_request',
            title='Demande Producteur',
            message=f"📄 <b>{instance.user.username}</b> a soumis une candidature pour devenir producteur.",
            link=reverse('admin_producer_requests')
        )

@receiver(post_save, sender=Show)
def notify_new_show(sender, instance, created, **kwargs):
    if created and instance.status == 'pending':
        producer_name = instance.producer.username if instance.producer else "Un producteur"
        Notification.objects.create(
            type='new_show',
            title='Nouveau Spectacle',
            message=f"🎬 <b>{producer_name}</b> a soumis le spectacle '<b>{instance.title}</b>' pour approbation.",
            link=reverse('admin_approve_show', args=[instance.pk])
        )
