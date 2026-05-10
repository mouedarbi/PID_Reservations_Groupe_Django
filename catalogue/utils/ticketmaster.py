import requests
from catalogue.models.setting import AppSetting

class TicketmasterAPI:
    ROOT_URL = "https://app.ticketmaster.com/discovery/v2/"

    def __init__(self):
        self.api_key = AppSetting.get_value('TICKETMASTER_API_KEY')

    def get_events(self, city=None, classification="Theatre", size=100, state_code=None):
        if not self.api_key:
            return None, "Erreur: Clé API Ticketmaster manquante."

        url = f"{self.ROOT_URL}events.json"
        params = {
            'apikey': self.api_key,
            'classificationName': classification,
            'size': size,
            'countryCode': 'BE',
            'locale': 'fr-be,*',
            'sort': 'date,asc'
        }
        
        if city:
            params['city'] = city
        if state_code:
            # Ticketmaster utilise parfois stateCode pour les provinces/régions
            params['stateCode'] = state_code

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

    yield "Recherche étendue des événements (Bruxelles, Forest, Laeken, Brabant Wallon)...\n"
    
    api = TicketmasterAPI()
    
    # Liste des zones à scanner pour maximiser les résultats
    zones = [
        {'city': 'Brussels'},
        {'city': 'Forest'},
        {'city': 'Laeken'},
        # Brabant Wallon
        {'city': 'Wavre'}, 
        {'city': 'Ottignies-Louvain-la-Neuve'}, 
        {'city': 'Waterloo'},
        # Flandre (Grandes villes)
        {'city': 'Antwerpen'}, # Anvers
        {'city': 'Gent'},      # Gand
        {'city': 'Brugge'},    # Bruges
        {'city': 'Leuven'},    # Louvain
        {'city': 'Mechelen'},  # Malines
        {'city': 'Hasselt'},
        {'city': 'Oostende'},  # Ostende
        {'city': 'Kortrijk'},  # Courtrai
        {'city': 'Aalst'},     # Alost
    ]
    
    all_events = []
    seen_ids = set()
    
    import time
    
    for zone in zones:
        yield f"Scan de la zone : {zone.get('city')}..."
        events, error = api.get_events(city=zone.get('city'), size=50)
        
        # Pause pour éviter l'erreur 429 (Rate Limit)
        time.sleep(0.5)
        
        if error:
            yield f" (Erreur : {error})\n"
            continue
            
        if events:
            new_in_zone = 0
            for e in events:
                if e['id'] not in seen_ids:
                    all_events.append(e)
                    seen_ids.add(e['id'])
                    new_in_zone += 1
            yield f" {new_in_zone} nouveaux événements trouvés.\n"
        else:
            yield " aucun résultat.\n"

    if not all_events:
        yield "Aucun événement trouvé pour les critères sélectionnés.\n"
        return

    yield f"\nTotal à traiter : {len(all_events)} événements.\n\n"
    
    count_new = 0
    count_updated = 0

    for event in all_events:
        name = event.get('name')
        yield f"Traitement de : {name}..."
        
        try:
            # 1. Localité - Sécurisation contre les doublons de CP
            venue_data = event.get('_embedded', {}).get('venues', [{}])[0]
            city_name = venue_data.get('city', {}).get('name', 'Bruxelles')
            postal_code = venue_data.get('postalCode', '1000')
            
            # On cherche d'abord s'il existe une localité avec ce CP et ce nom
            locality = Locality.objects.filter(postal_code=postal_code, locality__icontains=city_name).first()
            if not locality:
                # Sinon on prend juste par CP
                locality = Locality.objects.filter(postal_code=postal_code).first()
            
            if not locality:
                # Si vraiment rien, on crée
                locality = Locality.objects.create(postal_code=postal_code, locality=city_name, locality_fr=city_name)

            # 2. Lieu - Sécurisation du slug
            location_name = venue_data.get('name', 'Lieu inconnu')
            location_slug = slugify(location_name)[:60]
            
            location = Location.objects.filter(slug=location_slug).first()
            if not location:
                location = Location.objects.create(
                    slug=location_slug, 
                    designation=location_name, 
                    designation_fr=location_name, 
                    address=venue_data.get('address', {}).get('line1', ''), 
                    locality=locality
                )

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
