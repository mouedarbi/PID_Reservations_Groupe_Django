import re
import os

def count_msgids(file_path):
    if not os.path.exists(file_path):
        return 0
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    msgids = re.findall(r'msgid "(.*)"', content)
    msgids = [m for m in msgids if m] # filter out empty header msgid
    return len(set(msgids))

print(f"NL Unique msgids: {count_msgids('locale/nl/LC_MESSAGES/django.po')}")
print(f"EN Unique msgids: {count_msgids('locale/en/LC_MESSAGES/django.po')}")
