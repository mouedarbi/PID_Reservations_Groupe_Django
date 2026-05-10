import re
import os

def extract_msgids(file_path, output_file):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    msgids = re.findall(r'msgid "(.*)"', content)
    msgids = sorted(list(set([m for m in msgids if m])))
    with open(output_file, 'w', encoding='utf-8') as f:
        for m in msgids:
            f.write(m + '\n')

extract_msgids('locale/nl/LC_MESSAGES/django.po', 'msgids_to_translate.txt')
