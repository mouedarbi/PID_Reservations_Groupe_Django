from django.contrib.syndication.views import Feed
from django.urls import reverse
from catalogue.models import Representation
from django.utils import timezone
from django.utils.feedgenerator import Rss201rev2Feed

class LatestRepresentationsFeed(Feed):
    """
    Flux RSS standard 2.0 listant les prochaines représentations de spectacles.
    Répond aux exigences académiques de syndication de contenu.
    """
    feed_type = Rss201rev2Feed
    title = "Prochaines représentations - ThéâtrePlus"
    link = "/shows/"
    description = "La liste des 50 prochaines représentations à venir sur notre plateforme."
    language = "fr"

    def items(self):
        # On récupère les 50 prochaines représentations à partir de maintenant
        # select_related est crucial pour éviter le problème N+1 requêtes en DB
        return Representation.objects.filter(
            schedule__gte=timezone.now()
        ).select_related('show', 'location').order_by('schedule')[:50]

    def item_title(self, item):
        # Format : "Titre du spectacle (Lieu)"
        location_name = item.location.designation if item.location else "Lieu à confirmer"
        return f"{item.show.title} - {location_name}"

    def item_description(self, item):
        # Description riche incluant date et lien
        date_str = item.schedule.strftime('%d/%m/%Y à %H:%M')
        return (f"Le spectacle '{item.show.title}' aura lieu le {date_str}. "
                f"Lieu : {item.location.designation if item.location else 'Inconnu'}. "
                f"Places disponibles : {item.available_seats}")

    def item_link(self, item):
        # Utilise l'ID pour pointer vers le détail du spectacle
        # Feed() transforme automatiquement ceci en URL absolue si possible
        return reverse('frontend:show_detail', args=[item.show.id])

    def item_guid(self, item):
        # Identifiant unique pour les lecteurs RSS pour éviter les doublons
        return f"representation-{item.id}"

    def item_pubdate(self, item):
        # Dans ce contexte, la date de publication est la date de l'événement
        return item.schedule
