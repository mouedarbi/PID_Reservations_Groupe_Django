import requests
from catalogue.models.setting import AppSetting

class TicketmasterAPI:
    ROOT_URL = "https://app.ticketmaster.com/discovery/v2/"

    def __init__(self):
        self.api_key = AppSetting.get_value('TICKETMASTER_API_KEY')

    def get_events(self, city="Brussels", classification="Theatre", size=20):
        if not self.api_key:
            return None, "Erreur: Clé API Ticketmaster manquante."

        url = f"{self.ROOT_URL}events.json"
        params = {
            'apikey': self.api_key,
            'city': city,
            'classificationName': classification,
            'size': size,
            'countryCode': 'BE',
            'locale': 'fr-be,*'
        }

        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return data.get('_embedded', {}).get('events', []), None
            else:
                return None, f"Erreur API Ticketmaster ({response.status_code}): {response.text}"
        except Exception as e:
            return None, f"Erreur lors de l'appel Ticketmaster : {e}"

    @staticmethod
    def get_best_image(images):
        for img in images:
            if img.get('ratio') == '3_2' and img.get('width', 0) > 600:
                return img.get('url')
        return images[0].get('url') if images else None

def run_ticketmaster_import_gen():
    """
    Générateur pour importer les spectacles avec retour en temps réel.
    """
    from django.utils.text import slugify
    from django.utils.dateparse import parse_datetime
    from django.core.files.base import ContentFile
    from catalogue.models import Show, Location, Locality, Representation
    import datetime
    import requests
    import os

    yield "Initialisation de la connexion à Ticketmaster...\n"
    
    api = TicketmasterAPI()
    events, error = api.get_events()
    
    if error:
        yield f"ERREUR : {error}\n"
        return

    if not events:
        yield "Aucun événement trouvé pour les critères sélectionnés.\n"
        return

    yield f"Récupération de {len(events)} événements réussie.\n\n"
    
    count_new = 0
    count_updated = 0

    for event in events:
        name = event.get('name')
        yield f"Traitement de : {name}..."
        
        try:
            # 1. Localité
            venue_data = event.get('_embedded', {}).get('venues', [{}])[0]
            city_name = venue_data.get('city', {}).get('name', 'Bruxelles')
            postal_code = venue_data.get('postalCode', '1000')
            locality, _ = Locality.objects.get_or_create(postal_code=postal_code, defaults={'locality': city_name, 'locality_fr': city_name})

            # 2. Lieu
            location_name = venue_data.get('name', 'Lieu inconnu')
            location_slug = slugify(location_name)[:60]
            location, _ = Location.objects.get_or_create(slug=location_slug, defaults={'designation': location_name, 'designation_fr': location_name, 'address': venue_data.get('address', {}).get('line1', ''), 'locality': locality})

            # 3. Spectacle
            show_slug = slugify(name)[:60]
            
            # Récupérer l'URL de l'image
            poster_url = TicketmasterAPI.get_best_image(event.get('images', []))
            
            show, created = Show.objects.get_or_create(
                slug=show_slug,
                defaults={
                    'title': name, 'title_fr': name,
                    'description': event.get('info') or event.get('pleaseNote') or f"Spectacle : {name}",
                    'location': location, 'bookable': True, 'duration': 90,
                    'created_in': datetime.date.today().year,
                    'status': 'published',
                    'external_url': event.get('url')
                }
            )

            # Mettre à jour l'URL externe si elle n'existe pas déjà (pour les spectacles existants)
            if not created and not show.external_url and event.get('url'):
                show.external_url = event.get('url')
                show.save()

            # Si on a une URL d'image et que le spectacle n'a pas encore de poster
            if poster_url and not show.poster:
                try:
                    response = requests.get(poster_url, timeout=10)
                    if response.status_code == 200:
                        # Extraire l'extension du fichier
                        ext = os.path.splitext(poster_url.split('?')[0])[1] or '.jpg'
                        filename = f"{show_slug}{ext}"
                        show.poster.save(filename, ContentFile(response.content), save=True)
                except Exception as img_err:
                    yield f" (Erreur image : {img_err})"
            
            if created:
                count_new += 1
                yield " [NOUVEAU]\n"
            else:
                count_updated += 1
                yield " [EXISTANT]\n"

            # 4. Représentations
            start_data = event.get('dates', {}).get('start', {})
            local_date = start_data.get('localDate')
            if local_date:
                schedule = parse_datetime(f"{local_date}T{start_data.get('localTime', '20:00:00')}")
                if schedule:
                    _, rep_created = Representation.objects.get_or_create(show=show, schedule=schedule, defaults={'location': location, 'available_seats': 100})
                    if rep_created:
                        yield f"   -> Nouvelle date ajoutée : {local_date}\n"

        except Exception as e:
            yield f" [ERREUR : {str(e)}]\n"

    yield f"\nSynchronisation terminée !\n"
    yield f"Résultat : {count_new} créés, {count_updated} déjà présents.\n"

def run_ticketmaster_import():
    """Version originale pour compatibilité (non utilisée pour le live)"""
    gen = run_ticketmaster_import_gen()
    # On consomme tout le générateur sans rien afficher
    for _ in gen: pass
    return 0, 0 # Valeurs par défaut
