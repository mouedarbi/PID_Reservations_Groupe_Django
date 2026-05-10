import os

# Liste des traductions essentielles (Français -> Néerlandais)
translations_nl = {
    "Accueil": "Home",
    "Spectacles": "Voorstellingen",
    "Articles de presse": "Persartikelen",
    "Lieux": "Locaties",
    "À propos": "Over ons",
    "Mon compte": "Mijn account",
    "Mon profil": "Mijn profiel",
    "Dashboard Admin": "Admin Dashboard",
    "Espace Producteur": "Producentenruimte",
    "Mes articles": "Mijn artikelen",
    "Devenir Producteur": "Producent worden",
    "Déconnexion": "Uitloggen",
    "Connexion": "Inloggen",
    "Inscription": "Registreren",
    "Mon Panier": "Mijn Winkelmandje",
    "Nos Spectacles": "Onze Voorstellingen",
    "Explorez les événements à venir et réservez vos billets.": "Ontdek de komende evenementen en reserveer uw tickets.",
    "Lire la suite": "Lees meer",
    "Précédent": "Vorige",
    "Suivant": "Volgende",
    "Page": "Pagina",
    "sur": "van",
}

def fill_translations(file_path, trans_dict):
    if not os.path.exists(file_path):
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('msgid "'):
            msgid = line.split('"')[1]
            if msgid in trans_dict:
                new_lines.append(line)
                i += 1
                if i < len(lines) and lines[i].startswith('msgstr ""'):
                    new_lines.append(f'msgstr "{trans_dict[msgid]}"\n')
                    i += 1
                    continue
        new_lines.append(line)
        i += 1
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

# Appliquer les traductions
fill_translations('locale/nl/LC_MESSAGES/django.po', translations_nl)

# Ajouter aussi quelques traductions anglaises basiques
translations_en = {
    "Accueil": "Home",
    "Spectacles": "Shows",
    "Articles de presse": "Press Articles",
    "Lieux": "Locations",
    "À propos": "About",
    "Mon compte": "My account",
    "Mon profil": "My profile",
    "Mes articles": "My articles",
    "Devenir Producteur": "Become a Producer",
    "Déconnexion": "Logout",
    "Connexion": "Login",
    "Inscription": "Sign Up",
    "Mon Panier": "My Cart",
}
fill_translations('locale/en/LC_MESSAGES/django.po', translations_en)

print("Traductions essentielles injectées.")
