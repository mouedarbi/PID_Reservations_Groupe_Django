import os
import re

def fix_and_translate_po(file_path, translations):
    if not os.path.exists(file_path):
        return
    
    print(f"Processing {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split into entries
    # A standard entry starts with optional comments/references, then msgid, then msgstr
    entries = re.split(r'\n\n(?=msgid|#)', content)
    fixed_entries = []
    
    for entry in entries:
        if not entry.strip(): continue
        
        # Extract msgid
        msgid_match = re.search(r'msgid\s+((?:".*"\s*)+)', entry)
        if not msgid_match:
            fixed_entries.append(entry)
            continue
            
        msgid_raw = msgid_match.group(1).strip()
        # Clean the msgid to use as key (combine multi-line strings)
        msgid_key = "".join(re.findall(r'"(.*)"', msgid_raw))
        
        # Find msgstr
        msgstr_match = re.search(r'msgstr\s+((?:".*"\s*)*)', entry)
        
        if msgid_key in translations:
            new_msgstr = f'msgstr "{translations[msgid_key]}"'
            if msgstr_match:
                entry = entry.replace(msgstr_match.group(0), new_msgstr)
            else:
                entry += "\n" + new_msgstr
        elif not msgstr_match or not msgstr_match.group(1).strip():
            # Ensure msgstr exists even if empty
            if not msgstr_match:
                entry += '\nmsgstr ""'
            else:
                # msgstr exists but might be empty or missing quotes in a weird way
                pass
                
        fixed_entries.append(entry)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(fixed_entries) + '\n')

# Combined dictionary for all batches
all_nl = {}
# Import from batches
import translate_batch1, translate_batch2, translate_batch3, translate_batch4
all_nl.update(translate_batch1.batch1_nl)
all_nl.update(translate_batch2.batch2_nl)
all_nl.update(translate_batch3.batch3_nl)
all_nl.update(translate_batch4.batch4_nl)

all_en = {}
all_en.update(translate_batch1.batch1_en)
all_en.update(translate_batch2.batch2_en)
all_en.update(translate_batch3.batch3_en)
all_en.update(translate_batch4.batch4_en)

fix_and_translate_po('locale/nl/LC_MESSAGES/django.po', all_nl)
fix_and_translate_po('locale/en/LC_MESSAGES/django.po', all_en)

print("Final processing completed.")
