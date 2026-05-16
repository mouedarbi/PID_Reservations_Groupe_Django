import os
import sys
import django

# Ajout de la racine du projet au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reservations.settings')
django.setup()

from catalogue.models import Artist, Type, ArtistType, ArtistTypeShow, Show
from catalogue.utils.translation import translate_type, translate_text

def sync_artist_and_genre(full_name, show, genre_name):
    print(f"\n--- Synchronisation de l'artiste : {full_name} avec le genre : {genre_name} ---")
    
    # Séparation nom/prénom
    parts = full_name.split()
    if len(parts) > 1:
        firstname = " ".join(parts[:-1])
        lastname = parts[-1]
    else:
        firstname = full_name
        lastname = ""
    
    # 1. Artiste
    artist, _ = Artist.objects.get_or_create(firstname=firstname, lastname=lastname)
    
    # 2. Gestion intelligente du Type (Genre)
    # Traduire d'abord pour voir si une version FR existe déjà
    translated_fr = translate_text(genre_name, 'fr')
    
    # Chercher par nom original ou par traduction FR
    show_type = Type.objects.filter(type__iexact=genre_name).first()
    if not show_type:
        show_type = Type.objects.filter(type__iexact=translated_fr).first()
        
    if not show_type:
        print(f"Nouveau type à créer : {genre_name} (Traduction: {translated_fr})")
        show_type = Type.objects.create(type=genre_name)
        translate_type(show_type)
    else:
        print(f"Type existant trouvé : {show_type.type}")
        # Mettre à jour les traductions si vides
        if not show_type.type_en or not show_type.type_nl:
            translate_type(show_type)

    # 3. ArtistType (Lien Artiste-Genre)
    artist_type, _ = ArtistType.objects.get_or_create(artist=artist, type=show_type)
    
    # 4. Lien au Spectacle
    ats, created = ArtistTypeShow.objects.get_or_create(show=show, artist_type=artist_type)
    if created:
        print(f"Lien créé : {artist} est lié au type '{show_type.type}' pour le spectacle '{show.title}'")

if __name__ == "__main__":
    test_show = Show.objects.first()
    if test_show:
        print(f"Test avec le spectacle : {test_show.title}")
        # Simulation de données Ticketmaster
        sync_artist_and_genre("Haroun", test_show, "Comedy")
        sync_artist_and_genre("Houria les yeux verts", test_show, "Comedy")
