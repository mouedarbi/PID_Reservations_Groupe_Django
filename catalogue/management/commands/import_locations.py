import requests
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from catalogue.models import Location, Locality

class Command(BaseCommand):
    help = 'Importe des salles de concert et théâtres depuis l\'API ODWB'

    def handle(self, *args, **options):
        url = "https://www.odwb.be/api/explore/v2.1/catalog/datasets/salles-de-concert-et-theatres-en-wallonie-et-a-bruxelles/records?limit=100"
        
        self.stdout.write("Récupération des données depuis l'API...")
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            results = data.get('results', [])
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erreur lors de l'appel API : {e}"))
            return

        count_created = 0
        count_updated = 0

        for item in results:
            salle_name = item.get('salle')
            if not salle_name:
                continue

            # 1. Gérer la Localité (Locality)
            postal_code = str(item.get('code_postal', '')).strip()
            city_name = item.get('ville', '').strip()
            
            locality = None
            if postal_code and city_name:
                # Normalisation pour éviter les doublons de ville (ex: BRUXELLES vs Bruxelles)
                locality, _ = Locality.objects.get_or_create(
                    postal_code=postal_code,
                    locality=city_name
                )

            # 2. Gérer la Salle (Location)
            # On vérifie d'abord si elle existe par son nom (designation)
            existing_location = Location.objects.filter(designation=salle_name).first()
            
            if existing_location:
                # Mise à jour
                existing_location.address = item.get('adresse', '') or ''
                existing_location.locality = locality
                existing_location.website = item.get('site_web')
                existing_location.phone = item.get('telephone')
                existing_location.save()
                count_updated += 1
                self.stdout.write(f"Mis à jour : {salle_name}")
            else:
                # Création avec gestion du slug unique
                base_slug = slugify(salle_name)[:55]
                slug = base_slug
                counter = 1
                while Location.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                
                Location.objects.create(
                    slug=slug,
                    designation=salle_name,
                    address=item.get('adresse', '') or '',
                    locality=locality,
                    website=item.get('site_web'),
                    phone=item.get('telephone')
                )
                count_created += 1
                self.stdout.write(self.style.SUCCESS(f"Créé : {salle_name}"))

        self.stdout.write(self.style.SUCCESS(f"Terminé ! {count_created} créés, {count_updated} mis à jour."))
