def add_to_po(file_path, entries):
    with open(file_path, 'a', encoding='utf-8') as f:
        for fr, trans in entries:
            f.write(f'\nmsgid "{fr}"\nmsgstr "{trans}"\n')

en_entries = [
    ("PAYÉ", "PAID"),
    ("EN ATTENTE", "PENDING"),
    ("ÉCHOUÉ", "FAILED"),
    ("Nom d'utilisateur", "Username"),
    ("Email", "Email"),
    ("Langue préférée", "Preferred language"),
    ("Sécurité", "Security"),
    ("Modifier", "Edit"),
    ("Détails", "Details"),
]

nl_entries = [
    ("PAYÉ", "BETAALD"),
    ("EN ATTENTE", "IN AFWACHTING"),
    ("ÉCHOUÉ", "MISLUKT"),
    ("Nom d'utilisateur", "Gebruikersnaam"),
    ("Email", "Email"),
    ("Langue préférée", "Voorkeurstaal"),
    ("Sécurité", "Beveiliging"),
    ("Modifier", "Bewerken"),
    ("Détails", "Details"),
]

add_to_po('locale/en/LC_MESSAGES/django.po', en_entries)
add_to_po('locale/nl/LC_MESSAGES/django.po', nl_entries)
