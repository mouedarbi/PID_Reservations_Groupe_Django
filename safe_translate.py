import os
import re

def process_po_file(file_path, translations):
    if not os.path.exists(file_path):
        return
    
    print(f"Safe processing of {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        
        if line.startswith('msgid "'):
            # It's a msgid.
            # Handle multi-line msgid
            msgid_lines = [line]
            j = i + 1
            while j < len(lines) and lines[j].startswith('"'):
                msgid_lines.append(lines[j])
                j += 1
            
            # Reconstruct msgid key
            msgid_key = "".join([re.search(r'"(.*)"', l).group(1) for l in msgid_lines])
            
            # Find the corresponding msgstr
            # skip any comments between msgid and msgstr (though rare)
            k = j
            while k < len(lines) and not lines[k].startswith('msgstr'):
                k += 1
            
            if k < len(lines) and lines[k].startswith('msgstr'):
                # Found msgstr
                new_lines.extend(msgid_lines)
                # Fill msgstr if translation exists
                if msgid_key in translations:
                    new_lines.append(f'msgstr "{translations[msgid_key]}"\n')
                else:
                    new_lines.append(lines[k])
                
                # skip multi-line msgstr if any
                m = k + 1
                while m < len(lines) and lines[m].startswith('"'):
                    if msgid_key not in translations:
                        new_lines.append(lines[m])
                    m += 1
                i = m
                continue
            else:
                # No msgstr found after msgid! (Structural error)
                new_lines.extend(msgid_lines)
                if msgid_key in translations:
                    new_lines.append(f'msgstr "{translations[msgid_key]}"\n')
                else:
                    new_lines.append('msgstr ""\n')
                i = j
                continue
        
        new_lines.append(line)
        i += 1

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

# Combined dictionary for all batches
all_nl = {}
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

process_po_file('locale/nl/LC_MESSAGES/django.po', all_nl)
process_po_file('locale/en/LC_MESSAGES/django.po', all_en)
print("Safe translation applied.")
