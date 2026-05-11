import os
import sys
import django

# Ajouter la racine du projet au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reservations.settings')
django.setup()

import random
from django.contrib.auth.models import User, Group

def generate_members(count=90, start_idx=14):
    try:
        member_group, _ = Group.objects.get_or_create(name='MEMBER')
        
        # Listes de noms/prénoms pour le réalisme
        first_names_m = ["Jean", "Michel", "Pierre", "Philippe", "André", "Nicolas", "Christophe", "Marc", "Antoine", "Benoît", "Julien", "David", "Sébastien", "Laurent", "Frédéric"]
        first_names_f = ["Marie", "Nathalie", "Isabelle", "Catherine", "Sylvie", "Anne", "Françoise", "Monique", "Sandrine", "Valérie", "Sophie", "Julie", "Élodie", "Céline", "Camille"]
        last_names = ["Dubois", "Lefebvre", "Moreau", "Laurent", "Simon", "Michel", "Garcia", "Thomas", "Robert", "Gerard", "Petit", "Lucas", "Adam", "Lambert", "Mercier"]

        created_count = 0
        for i in range(start_idx, start_idx + count):
            username = f"membre{i:02d}"
            
            # 60% Masculin, 40% Féminin
            is_male = random.random() < 0.6
            first_name = random.choice(first_names_m if is_male else first_names_f)
            last_name = random.choice(last_names)
            email = f"{username}@example.com"
            
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password='theatreplus01',
                    first_name=first_name,
                    last_name=last_name
                )
                user.groups.add(member_group)
                created_count += 1
                
        print(f"Succès : {created_count} nouveaux membres créés.")
        
    except Exception as e:
        print(f"Erreur lors de la génération : {e}")

if __name__ == "__main__":
    # On commence à 14 car mebre05, membre01, membre02 existent déjà ou sont proches
    generate_members(90, 14)
    # Créer les membres manquants entre 03 et 13
    generate_members(11, 3)
