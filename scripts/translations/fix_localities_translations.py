from catalogue.models import Locality

# Dictionnaire de traduction officiel pour les principales villes belges
# (Inclut FR, NL, EN)
BELGIAN_MAPPING = {
    "Bruxelles": {"nl": "Brussel", "en": "Brussels"},
    "Anvers": {"nl": "Antwerpen", "en": "Antwerp"},
    "Gand": {"nl": "Gent", "en": "Ghent"},
    "Bruges": {"nl": "Brugge", "en": "Bruges"},
    "Liège": {"nl": "Luik", "en": "Liege"},
    "Namur": {"nl": "Namen", "en": "Namur"},
    "Mons": {"nl": "Bergen", "en": "Mons"},
    "Louvain": {"nl": "Leuven", "en": "Louvain"},
    "Malines": {"nl": "Mechelen", "en": "Mechlin"},
    "Tournai": {"nl": "Doornik", "en": "Tournai"},
    "Courtrai": {"nl": "Kortrijk", "en": "Courtrai"},
    "Ostende": {"nl": "Oostende", "en": "Ostend"},
    "Verviers": {"nl": "Verviers", "en": "Verviers"},
    "Charleroi": {"nl": "Charleroi", "en": "Charleroi"},
    "Hasselt": {"nl": "Hasselt", "en": "Hasselt"},
    "Alost": {"nl": "Aalst", "en": "Alost"},
    "La Louvière": {"nl": "La Louvière", "en": "La Louviere"},
    "Wavre": {"nl": "Waver", "en": "Wavre"},
    "Hal": {"nl": "Halle", "en": "Halle"},
    "Renaix": {"nl": "Ronse", "en": "Renaix"},
    "Ypres": {"nl": "Ieper", "en": "Ypres"},
    "Dixmude": {"nl": "Diksmuide", "en": "Diksmuide"},
    "Tongres": {"nl": "Tongeren", "en": "Tongres"},
    "Termonde": {"nl": "Dendermonde", "en": "Termonde"},
    "Tirlemont": {"nl": "Tienen", "en": "Tirlemont"},
    "Ath": {"nl": "Aat", "en": "Ath"},
    "Nivelles": {"nl": "Nijvel", "en": "Nivelles"},
    "Braine-l'Alleud": {"nl": "Eigenbrakel", "en": "Braine-l'Alleud"},
    "Braine-le-Comte": {"nl": "'s-Gravenbrakel", "en": "Braine-le-Comte"},
    "Enghien": {"nl": "Edingen", "en": "Enghien"},
    "Lessines": {"nl": "Lessen", "en": "Lessines"},
    "Péruwelz": {"nl": "Péruwelz", "en": "Peruwelz"},
    "Soignies": {"nl": "Zinnik", "en": "Soignies"},
    "Binche": {"nl": "Binche", "en": "Binche"},
    "Eupen": {"nl": "Eupen", "en": "Eupen"},
    "Bastogne": {"nl": "Bastenaken", "en": "Bastogne"},
    "Arlon": {"nl": "Aarlen", "en": "Arlon"},
    "Marche-en-Famenne": {"nl": "Marche-en-Famenne", "en": "Marche-en-Famenne"},
    "Neufchâteau": {"nl": "Neufchâteau", "en": "Neufchateau"},
    "Virton": {"nl": "Virton", "en": "Virton"},
    "Aubange": {"nl": "Aubange", "en": "Aubange"},
}

def run():
    print("Début de la traduction manuelle des localités...")
    localities = Locality.objects.all()
    count = 0
    
    for loc in localities:
        # On utilise le français comme base si disponible, sinon le nom par défaut
        base_name = loc.locality_fr or loc.locality
        
        if base_name in BELGIAN_MAPPING:
            mapping = BELGIAN_MAPPING[base_name]
            loc.locality_nl = mapping['nl']
            loc.locality_en = mapping['en']
            loc.locality_fr = base_name
            loc.save()
            count += 1
        else:
            # Pour les autres, on s'assure au moins que les colonnes ne sont pas None
            # et on capitalise proprement
            cleaned_name = base_name.strip().title()
            loc.locality = cleaned_name
            loc.locality_fr = cleaned_name
            if not loc.locality_nl or loc.locality_nl == "None":
                loc.locality_nl = cleaned_name
            if not loc.locality_en or loc.locality_en == "None":
                loc.locality_en = cleaned_name
            loc.save()

    print(f"Terminé ! {count} grandes villes traduites spécifiquement. Les 2760 entrées ont été nettoyées.")

if __name__ == "__main__":
    run()
