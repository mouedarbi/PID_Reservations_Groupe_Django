import os
import sys
import django
from django.db import transaction

# Ajout de la racine du projet au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reservations.settings')
django.setup()

from catalogue.models import Type, ArtistType

def cleanup_duplicate_types():
    print("--- Début du nettoyage des types en double ---")
    
    # Trouver les noms de types qui apparaissent plus d'une fois
    from django.db.models import Count
    duplicate_names = Type.objects.values('type').annotate(count=Count('id')).filter(count__gt=1)
    
    for entry in duplicate_names:
        type_name = entry['type']
        print(f"\nTraitement du type : '{type_name}' ({entry['count']} occurrences)")
        
        # Récupérer tous les objets Type portant ce nom, triés par ID
        types = list(Type.objects.filter(type=type_name).order_by('id'))
        keep_type = types[0]
        duplicates_to_remove = types[1:]
        
        print(f"  On garde l'ID {keep_type.id}")
        
        for dup in duplicates_to_remove:
            print(f"  Traitement du doublon ID {dup.id}...")
            
            # Mettre à jour les ArtistType qui pointent vers ce doublon
            related_count = ArtistType.objects.filter(type=dup).count()
            if related_count > 0:
                print(f"    Migration de {related_count} liens ArtistType vers l'ID {keep_type.id}")
                ArtistType.objects.filter(type=dup).update(type=keep_type)
            
            # Supprimer le doublon
            dup.delete()
            print(f"    Doublon ID {dup.id} supprimé.")

    print("\n--- Nettoyage terminé ---")

if __name__ == "__main__":
    with transaction.atomic():
        cleanup_duplicate_types()
