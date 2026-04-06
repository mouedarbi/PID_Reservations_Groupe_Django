import os
import re

def extract_strings(directory):
    strings = set()
    # Pattern for {% trans "..." %} or {% trans '...' %}
    trans_pattern = re.compile(r'{%\s+trans\s+["\'](.*?)["\']\s+%}')
    # Pattern for {% blocktrans %}...{% endblocktrans %}
    blocktrans_pattern = re.compile(r'{%\s+blocktrans.*?%}(.*?){%\s+endblocktrans\s+%}', re.DOTALL)
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    content = f.read()
                    strings.update(trans_pattern.findall(content))
                    for bt in blocktrans_pattern.findall(content):
                        # Clean up blocktrans content (remove extra whitespace/newlines)
                        strings.add(bt.strip())
    return strings

def update_po(file_path, new_strings):
    if not os.path.exists(file_path):
        print(f"File {file_path} not found.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    existing_ids = set(re.findall(r'msgid "(.*?)"', content))
    
    with open(file_path, 'a', encoding='utf-8') as f:
        for s in sorted(new_strings):
            if s and s not in existing_ids:
                f.write(f'\nmsgid "{s}"\nmsgstr ""\n')
                print(f"Added to {file_path}: {s}")
                existing_ids.add(s)

# Scan multiple directories
all_strings = set()
for d in ['frontend/templates', 'catalogue/templates', 'cart/templates', 'accounts/templates', 'templates']:
    if os.path.exists(d):
        all_strings.update(extract_strings(d))

update_po('locale/en/LC_MESSAGES/django.po', all_strings)
update_po('locale/nl/LC_MESSAGES/django.po', all_strings)
