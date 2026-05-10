from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from catalogue.models import ProducerRequest, Show, Notification, CriticRequest, PressArticle
from django.urls import reverse

@receiver(post_save, sender=User)
def notify_new_user(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            type='new_user',
            title='Nouvel Utilisateur',
            message=f"<b>{instance.username}</b> vient de rejoindre ThéâtrePlus ! Bienvenue à notre nouveau membre.",
            link=reverse('admin_user_index')
        )

@receiver(post_save, sender=ProducerRequest)
def notify_producer_request(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            type='producer_request',
            title='Demande Producteur',
            message=f"<b>{instance.user.username}</b> a soumis une candidature pour devenir producteur.",
            link=reverse('admin_producer_requests')
        )

@receiver(post_save, sender=CriticRequest)
def notify_critic_request(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            type='critic_request',
            title='Demande Critique',
            message=f"<b>{instance.user.username}</b> souhaite devenir critique de presse pour ThéâtrePlus.",
            link=reverse('admin_critic_requests')
        )

@receiver(post_save, sender=Show)
def notify_new_show(sender, instance, created, **kwargs):
    if created and instance.status == 'pending':
        producer_name = instance.producer.username if instance.producer else "Un producteur"
        Notification.objects.create(
            type='new_show',
            title='Nouveau Spectacle',
            message=f"<b>{producer_name}</b> a soumis le spectacle '<b>{instance.title}</b>' pour approbation.",
            link=reverse('admin_approve_show', args=[instance.pk])
        )

@receiver(post_save, sender=PressArticle)
def notify_new_press_article(sender, instance, created, **kwargs):
    if created:
        critic_name = instance.user.get_full_name() or instance.user.username
        
        # On notifie le producteur du spectacle
        if instance.show.producer:
            Notification.objects.create(
                user=instance.show.producer,
                type='new_article',
                title='Nouvel Article à Valider',
                message=f"<b>{critic_name}</b> a rédigé un article sur votre spectacle '<b>{instance.show.title}</b>'.",
                link=reverse('catalogue:prod_moderate_press_articles')
            )

