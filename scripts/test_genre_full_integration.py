import os
import sys
import django

# Ajout de la racine du projet au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reservations.settings')
django.setup()

from catalogue.models import Genre, Show, Location, Locality

def test_genre_crud_and_link():
    print("--- Test CRUD Genre et Liaison Spectacle ---")
    
    # 1. Création d'un Genre
    genre_name = "Drame Psychologique"
    genre, created = Genre.objects.get_or_create(
        name=genre_name,
        defaults={
            'name_fr': "Drame Psychologique",
            'name_en': "Psychological Drama",
            'name_nl': "Psychologisch Drama"
        }
    )
    if created:
        print(f"Genre créé : {genre}")
    else:
        print(f"Genre existant : {genre}")

    # 2. Vérification de la liaison dans un Show
    # On récupère un lieu pour le spectacle
    location = Location.objects.first()
    if not location:
        # Création d'un lieu fictif si nécessaire
        locality, _ = Locality.objects.get_or_create(postal_code="1000", defaults={'locality': "Bruxelles"})
        location = Location.objects.create(slug="lieu-test", designation="Lieu de Test", locality=locality)

    show_title = "Le Test Final"
    show, s_created = Show.objects.get_or_create(
        slug="le-test-final",
        defaults={
            'title': show_title,
            'title_fr': show_title,
            'location': location,
            'genre': genre,
            'bookable': True,
            'created_in': 2026
        }
    )
    
    if s_created:
        print(f"Spectacle créé et lié au genre : {show.genre}")
    else:
        # Mise à jour si déjà existant
        show.genre = genre
        show.save()
        print(f"Spectacle mis à jour avec le genre : {show.genre}")

    # 3. Vérification finale
    assert show.genre.name == genre_name
    print("\n--- Test réussi ! ---")

if __name__ == "__main__":
    test_genre_crud_and_link()
