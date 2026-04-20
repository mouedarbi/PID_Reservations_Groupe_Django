from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.utils.dateparse import parse_datetime
from catalogue.models import Show, Location, Locality, Artist, Type, ArtistType, Representation, Price, ShowPrice
from catalogue.utils.ticketmaster import TicketmasterAPI
import datetime

class Command(BaseCommand):
    help = 'Importe des spectacles de theatre depuis Ticketmaster'

    def handle(self, *args, **options):
        api = TicketmasterAPI()
        self.stdout.write("Recuperation des evenements Ticketmaster...")
        events = api.get_events()

        if not events:
            self.stdout.write(self.style.WARNING("Aucun evenement trouve ou erreur API."))
            return

        for event in events:
            self.import_event(event)

        self.stdout.write(self.style.SUCCESS(f"Importation terminee : {len(events)} evenements traites."))

    def import_event(self, event):
        name = event.get('name')
        tm_id = event.get('id')
        self.stdout.write(f"Traitement de : {name}...")

        # 1. Gestion de la Localite (City)
        venue_data = event.get('_embedded', {}).get('venues', [{}])[0]
        city_name = venue_data.get('city', {}).get('name', 'Bruxelles')
        postal_code = venue_data.get('postalCode', '1000')
        
        locality, _ = Locality.objects.get_or_create(
            postal_code=postal_code,
            defaults={'locality': city_name, 'locality_fr': city_name}
        )

        # 2. Gestion du Lieu (Location)
        location_name = venue_data.get('name', 'Lieu inconnu')
        location_slug = slugify(location_name)[:60]
        address = venue_data.get('address', {}).get('line1', '')
        website = venue_data.get('url')

        location, _ = Location.objects.get_or_create(
            slug=location_slug,
            defaults={
                'designation': location_name,
                'designation_fr': location_name,
                'address': address,
                'address_fr': address,
                'locality': locality,
                'website': website
            }
        )

        # 3. Gestion du Spectacle (Show)
        # On utilise uniquement le nom pour le slug afin de regrouper les seances
        show_slug = slugify(name)[:60]
        description = event.get('info') or event.get('pleaseNote') or f"Spectacle de theatre : {name}"
        poster_url = TicketmasterAPI.get_best_image(event.get('images', []))

        show, created = Show.objects.get_or_create(
            slug=show_slug,
            defaults={
                'title': name,
                'title_fr': name,
                'description': description,
                'description_fr': description,
                'poster': poster_url,
                'location': location,
                'bookable': True,
                'duration': 90, # Par defaut
                'created_in': datetime.date.today().year
            }
        )
        if created:
            self.stdout.write(f"  - Nouveau spectacle cree : {name}")
        else:
            self.stdout.write(f"  - Spectacle existant trouve : {name}")

        # 4. Gestion des Artistes et Types
        attractions = event.get('_embedded', {}).get('attractions', [])
        for att in attractions:
            att_name = att.get('name')
            if not att_name: continue
            
            # Separation prenom/nom basique
            parts = att_name.split(' ', 1)
            first = parts[0]
            last = parts[1] if len(parts) > 1 else ''
            
            artist, _ = Artist.objects.get_or_create(
                firstname=first,
                lastname=last
            )

            # Type d'artiste (ex: comedien)
            artist_type_name = att.get('classifications', [{}])[0].get('segment', {}).get('name', 'Arts')
            type_obj, _ = Type.objects.get_or_create(
                type=artist_type_name.lower(),
                defaults={'type_fr': artist_type_name}
            )

            # Liaison ArtistType
            ArtistType.objects.get_or_create(artist=artist, type=type_obj)

        # 5. Gestion de la Representation
        start_data = event.get('dates', {}).get('start', {})
        local_date = start_data.get('localDate')
        local_time = start_data.get('localTime', '20:00:00')
        
        if local_date:
            schedule_str = f"{local_date}T{local_time}"
            schedule = parse_datetime(schedule_str)
            if schedule:
                Representation.objects.get_or_create(
                    show=show,
                    schedule=schedule,
                    defaults={'location': location, 'available_seats': 100}
                )

        # 6. Gestion des Prix
        price_ranges = event.get('priceRanges', [])
        for pr in price_ranges:
            price_val = pr.get('min')
            if price_val:
                price_obj, _ = Price.objects.get_or_create(
                    type="Standard",
                    price=price_val,
                    defaults={'description': 'Tarif Ticketmaster'}
                )
                ShowPrice.objects.get_or_create(show=show, price=price_obj)
