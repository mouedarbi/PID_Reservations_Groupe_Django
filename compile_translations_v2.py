import os
try:
    import polib
except ImportError:
    print("polib is not installed. Installing it...")
    os.system("pip install polib")
    import polib

def compile_po(po_file):
    mo_file = po_file.replace('.po', '.mo')
    try:
        po = polib.pofile(po_file)
        po.save_as_mofile(mo_file)
        print(f"Successfully compiled {po_file} to {mo_file}")
        # Count translated vs untranslated
        translated = len(po.translated_entries())
        untranslated = len(po.untranslated_entries())
        print(f"  - Translated: {translated}, Untranslated: {untranslated}")
    except Exception as e:
        print(f"Error compiling {po_file}: {e}")

# Walk through locale directory
locale_dir = 'locale'
for root, dirs, files in os.walk(locale_dir):
    for file in files:
        if file.endswith('.po'):
            compile_po(os.path.join(root, file))
