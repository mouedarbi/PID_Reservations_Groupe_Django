import os
import django
from django.utils import timezone

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reservations.settings')
django.setup()

from catalogue.models import Show, Representation

def check_availability():
    now = timezone.now()
    print(f"Heure actuelle (UTC): {now}")
    print("-" * 50)
    
    shows = Show.objects.filter(status='published')
    if not shows.exists():
        print("Aucun spectacle publié trouvé.")
        return

    for s in shows:
        next_reps = s.representations.filter(schedule__gte=now)
        available_seats_total = sum(r.available_seats for r in next_reps)
        
        print(f"Spectacle: {s.title}")
        print(f"  - ID: {s.id}")
        print(f"  - Flag manuel 'bookable': {s.bookable}")
        print(f"  - Nombre de représentations à venir: {next_reps.count()}")
        print(f"  - Places disponibles totales (futures): {available_seats_total}")
        
        if next_reps.count() == 0:
            print("  -> Statut: COMPLET (Aucune séance future)")
        elif available_seats_total <= 0:
            print("  -> Statut: COMPLET (Plus de places dans les séances futures)")
        elif not s.bookable:
            print("  -> Statut: COMPLET (Désactivé manuellement)")
        else:
            print("  -> Statut: DISPONIBLE")
        print("-" * 50)

if __name__ == "__main__":
    check_availability()
