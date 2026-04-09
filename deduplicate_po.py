import os

def deduplicate_po(file_path):
    if not os.path.exists(file_path):
        print(f"File {file_path} not found.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    header = []
    entries = []
    current_entry = []
    
    # Simple state machine to parse entries
    # Entries start with msgid
    
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('msgid ""') and i + 1 < len(lines) and lines[i+1].startswith('msgstr ""'):
            # This is likely the header
            header.append(line)
            i += 1
            while i < len(lines) and (lines[i].startswith('msgstr') or lines[i].startswith('"')):
                header.append(lines[i])
                i += 1
            continue
        
        if line.startswith('msgid'):
            if current_entry:
                entries.append(current_entry)
            current_entry = [line]
        elif current_entry:
            current_entry.append(line)
        else:
            header.append(line)
        i += 1
    
    if current_entry:
        entries.append(current_entry)

    seen_msgids = set()
    unique_entries = []
    
    for entry in entries:
        # Extract msgid
        msgid_lines = []
        for line in entry:
            if line.startswith('msgid'):
                msgid_lines.append(line)
            elif line.startswith('"') and not any(l.startswith('msgstr') for l in entry[:entry.index(line)]):
                # Continuation of msgid
                msgid_lines.append(line)
            elif line.startswith('msgstr'):
                break
        
        msgid = "".join(msgid_lines)
        if msgid not in seen_msgids:
            seen_msgids.add(msgid)
            unique_entries.append(entry)
        else:
            print(f"Duplicate found in {file_path}: {msgid.strip()}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(header)
        for entry in unique_entries:
            f.writelines(entry)

deduplicate_po('locale/en/LC_MESSAGES/django.po')
deduplicate_po('locale/nl/LC_MESSAGES/django.po')
