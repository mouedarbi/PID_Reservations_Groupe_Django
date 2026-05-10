import os

def fix_po_structure(file_path):
    if not os.path.exists(file_path):
        return
    
    print(f"Fixing structure of {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    fixed_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        fixed_lines.append(line)
        
        # Si on trouve un msgid, on vérifie s'il y a un msgstr après
        if line.startswith('msgid "'):
            # Chercher la fin du msgid (peut être sur plusieurs lignes)
            j = i + 1
            while j < len(lines) and lines[j].startswith('"'):
                fixed_lines.append(lines[j])
                j += 1
            
            # Vérifier si la ligne suivante est un msgstr
            if j >= len(lines) or not lines[j].startswith('msgstr'):
                print(f"  Missing msgstr for msgid at line {i+1}. Adding empty one.")
                fixed_lines.append('msgstr ""\n')
            
            i = j - 1 # Sauter les lignes traitées
        i += 1
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)

# Réparer les fichiers
fix_po_structure('locale/nl/LC_MESSAGES/django.po')
fix_po_structure('locale/en/LC_MESSAGES/django.po')

print("Fichiers .po réparés.")
