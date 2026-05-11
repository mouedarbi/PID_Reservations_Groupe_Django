import re

input_file = 'reservation_wip_dump.sql'
output_file = 'reservation_final_dump.sql'

with open(input_file, 'r', encoding='utf-16') as f:
    content = f.read()

# 1. Remplacer le nom de la base de données
content = content.replace('reservation_wip_groupe', 'reservation_final')

# 2. Identifier les colonnes qui doivent être NULLABLE pour supporter SET NULL
# On cible spécifiquement les colonnes user_id dans reviews et press_articles
content = re.sub(r'(`user_id` int) NOT NULL', r'\1 DEFAULT NULL', content)
content = re.sub(r'(`producer_id` int) NOT NULL', r'\1 DEFAULT NULL', content)

# 3. Fonction pour appliquer les contraintes d'intégrité chirurgicalement
def apply_smart_constraints(match):
    constraint_line = match.group(0)
    
    # Liste des colonnes devant utiliser SET NULL (Anonymisation RGPD)
    set_null_cols = ['`user_id`', '`producer_id`', '`location_id`', '`locality_id`']
    
    # Si la contrainte porte sur une de ces colonnes, on met SET NULL
    if any(col in constraint_line for col in set_null_cols):
        # On vérifie si la ligne se termine par une virgule
        comma = "," if constraint_line.strip().endswith(",") else ""
        # On retire la virgule pour le replacement propre
        base = constraint_line.strip().rstrip(",")
        return f"  {base} ON DELETE SET NULL ON UPDATE CASCADE{comma}\n"
    else:
        # Sinon on met CASCADE par défaut (comportement standard Django)
        comma = "," if constraint_line.strip().endswith(",") else ""
        base = constraint_line.strip().rstrip(",")
        return f"  {base} ON DELETE CASCADE ON UPDATE CASCADE{comma}\n"

# Regex pour capturer les lignes CONSTRAINT ... FOREIGN KEY ... REFERENCES ...
pattern = r'^\s*CONSTRAINT\s+`[^`]+`\s+FOREIGN\s+KEY\s+\(`[^`]+`\)\s+REFERENCES\s+`[^`]+`\s+\(`[^`]+`\)(,)?'
content = re.sub(pattern, apply_smart_constraints, content, flags=re.MULTILINE)

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Fichier {output_file} généré avec succès avec gestion RGPD (SET NULL/CASCADE).")
