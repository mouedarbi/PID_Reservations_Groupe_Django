import sys
import os

def clean_duplicates(file_path):
    if not os.path.exists(file_path):
        print(f"File {file_path} not found.")
        return

    print(f"Cleaning duplicates in {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by entries (separated by empty lines)
    entries = content.split('\n\n')
    seen_msgids = set()
    unique_entries = []

    header = entries[0]
    unique_entries.append(header)
    
    # Start from index 1 to skip header
    for entry in entries[1:]:
        if not entry.strip():
            continue
            
        lines = entry.strip().split('\n')
        msgid_line = None
        for line in lines:
            if line.startswith('msgid "'):
                msgid_line = line
                break
        
        if msgid_line:
            if msgid_line not in seen_msgids:
                seen_msgids.add(msgid_line)
                unique_entries.append(entry.strip())
            else:
                print(f"  Removing duplicate: {msgid_line}")
        else:
            unique_entries.append(entry.strip())

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(unique_entries) + '\n')

if __name__ == "__main__":
    clean_duplicates('locale/en/LC_MESSAGES/django.po')
    clean_duplicates('locale/nl/LC_MESSAGES/django.po')
