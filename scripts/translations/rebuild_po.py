import os
import re

def rebuild_po(file_path, lang_name):
    if not os.path.exists(file_path):
        return
    
    print(f"Rebuilding {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract all msgid/msgstr pairs using regex
    # Handles multi-line strings
    pattern = r'msgid\s+((?:".*"\s*)+)\s+msgstr\s+((?:".*"\s*)+)'
    matches = re.findall(pattern, content)
    
    seen_ids = set()
    unique_pairs = []
    
    # Header pair is usually the first one (empty msgid)
    for msgid, msgstr in matches:
        if msgid not in seen_ids:
            seen_ids.add(msgid)
            unique_pairs.append((msgid.strip(), msgstr.strip()))
    
    with open(file_path, 'w', encoding='utf-8') as f:
        # Standard PO header if not present
        if not seen_ids or '""' not in seen_ids:
            f.write('msgid ""\nmsgstr ""\n"Content-Type: text/plain; charset=UTF-8\\n"\n"Content-Transfer-Encoding: 8bit\\n"\n\n')
            
        for msgid, msgstr in unique_pairs:
            f.write(f"msgid {msgid}\nmsgstr {msgstr}\n\n")

# Rebuild
rebuild_po('locale/nl/LC_MESSAGES/django.po', 'nl')
rebuild_po('locale/en/LC_MESSAGES/django.po', 'en')

print("Fichiers .po reconstruits.")
