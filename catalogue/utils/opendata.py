import requests
from django.utils.text import slugify
from catalogue.models import Location, Locality

class OpenDataAPI:
    """
    Client pour l'API OpenData Wallonie-Bruxelles (ODWB).
    """
    URL = "https://www.odwb.be/api/explore/v2.1/catalog/datasets/salles-de-concert-et-theatres-en-wallonie-et-a-bruxelles/records"

    def get_locations(self, limit=100):
        params = {
            'limit': limit
        }
        try:
            response = requests.get(self.URL, params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()
                return data.get('results', []), None
            else:
                return None, f"Erreur API OpenData ({response.status_code}): {response.text}"
        except Exception as e:
            return None, f"Erreur lors de l'appel OpenData : {e}"

def run_opendata_import_gen():
    """
    Générateur pour importer les lieux avec retour en temps réel (streaming).
    """
    api = OpenDataAPI()
    results, error = api.get_locations(limit=100)
    
    if error:
        yield f"ERREUR : {error}\n"
        return

    if not results:
        yield "Aucun lieu trouvé dans le jeu de données.\n"
        return

    yield f"Récupération de {len(results)} lieux réussie.\n\n"
    
    count_new = 0
    count_skipped = 0

    for item in results:
        name = item.get('salle')
        if not name:
            continue
            
        yield f"Traitement de : {name}..."
        
        try:
            # 1. Préparation du slug
            slug = slugify(name)[:60]
            website = item.get('site_web')
            
            # 2. Vérification si le lieu existe déjà (slug + website unique)
            if Location.objects.filter(slug=slug).exists():
                count_skipped += 1
                yield " [DÉJÀ PRÉSENT - Passé]\n"
                continue

            # 3. Gestion de la localité
            city_name = item.get('ville', 'Inconnue')
            postal_code = str(int(item.get('code_postal', 0))) if item.get('code_postal') else '0000'
            
            locality, _ = Locality.objects.get_or_create(
                postal_code=postal_code, 
                defaults={
                    'locality': city_name, 
                    'locality_fr': city_name
                }
            )

            # 4. Création du lieu
            location = Location.objects.create(
                slug=slug,
                designation=name,
                address=item.get('adresse', ''),
                locality=locality,
                website=website,
                phone=item.get('telephone'),
                capacity=int(item.get('jauge_maximale', 0))
            )
            
            count_new += 1
            yield " [IMPORTÉ]\n"

        except Exception as e:
            yield f" [ERREUR : {str(e)}]\n"

    yield f"\nImportation terminée !\n"
    yield f"Résultat : {count_new} nouveaux lieux importés, {count_skipped} ignorés.\n"
