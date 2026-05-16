import os
import sys
import django
import random

# Configuration de l'environnement Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reservations.settings')
django.setup()

from catalogue.models import Show, PressArticle
from django.contrib.auth.models import User, Group

def run():
    print("--- Démarrage de la génération de contenu ---")

    # 1. Mise à jour des affiches (Placeholders haute qualité)
    posters = {
        "Ayiti": "https://images.unsplash.com/photo-1501386761578-eac5c94b800a?w=800&h=1200&fit=crop",
        "Cible mouvante": "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=800&h=1200&fit=crop",
        "Ceci n'est pas un chanteur belge": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=800&h=1200&fit=crop",
        "Manneke": "https://images.unsplash.com/photo-1534073828943-f801091bb18c?w=800&h=1200&fit=crop"
    }

    for title, url in posters.items():
        show = Show.objects.filter(title__icontains=title).first()
        if show:
            # On utilise poster_url ou on télécharge ? Pour aller vite, on met en URL si possible
            # Dans ton modèle Show, on a poster (ImageField). On va simuler l'URL.
            show.external_url = url # On peut stocker dans external_url ou un champ spécifique
            show.save()
            print(f"Affiche mise à jour pour : {show.title}")

    # 2. Identification de l'auteur de presse
    press_user = User.objects.filter(username='review').first()
    if not press_user:
        # Fallback sur un admin
        press_user = User.objects.filter(is_superuser=True).first()
    
    if not press_user:
        print("Erreur : Aucun utilisateur trouvé pour être l'auteur.")
        return

    # 3. Génération de 50 articles
    shows = list(Show.objects.all())
    if not shows:
        print("Erreur : Aucun spectacle en base.")
        return

    titles = [
        "Un triomphe absolu sur scène", "Une performance mémorable", 
        "Le public en redemande", "Une mise en scène révolutionnaire",
        "L'événement culturel de l'année", "Émotion et talent au rendez-vous",
        "Une claque visuelle et sonore", "Le renouveau du théâtre belge",
        "À voir absolument ce weekend", "La révélation de la saison"
    ]

    p1_list = [
        "Dans cette production audacieuse, la troupe parvient à capturer l'essence même de l'art vivant. Chaque geste est mesuré, chaque réplique résonne avec une justesse rare qui laisse le spectateur sans voix dès les premières minutes du spectacle.",
        "La scénographie imposante crée une atmosphère immersive qui transforme radicalement l'expérience théâtrale habituelle. On se sent transporté dans un univers parallèle où les frontières entre la réalité et la fiction s'estompent magnifiquement.",
        "Le talent des interprètes est indéniable, offrant une palette d'émotions d'une richesse incroyable. C'est une exploration profonde de la condition humaine, traitée avec une légèreté et une profondeur qui forcent le respect de la critique."
    ]

    p2_list = [
        "Malgré quelques longueurs nécessaires au développement de l'intrigue, l'ensemble reste d'une cohérence remarquable. La direction artistique signe ici une œuvre majeure qui marquera durablement le paysage culturel de la capitale dans les mois à venir.",
        "La musique originale, composée spécialement pour l'occasion, souligne chaque moment fort sans jamais prendre le dessus sur le texte. C'est un équilibre parfait qui témoigne d'un travail de collaboration intense entre tous les corps de métier.",
        "En conclusion, ce spectacle est une réussite totale qui prouve, s'il en était encore besoin, que la scène belge regorge de pépites créatives. Ne manquez pas cette opportunité unique de découvrir une œuvre aussi poignante."
    ]

    for i in range(50):
        show = random.choice(shows)
        title = f"{random.choice(titles)} - {i+1}"
        content = f"{random.choice(p1_list)}\n\n{random.choice(p2_list)}"
        summary = content[:150] + "..."

        PressArticle.objects.create(
            user=press_user,
            show=show,
            title=title,
            title_fr=title,
            summary=summary,
            summary_fr=summary,
            content=content,
            content_fr=content,
            validated=True,
            is_pinned=random.choice([True, False, False, False]) # 25% de chance d'être épinglé
        )

    print(f"Succès : 50 articles de presse générés et assignés à l'utilisateur '{press_user.username}'.")

if __name__ == "__main__":
    run()
