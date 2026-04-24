import os

translations = [
    # Sidebar & Dashboard
    ("Accès API", "API Access", "API Toegang"),
    ("Ma Consommation", "My Usage", "Mijn Verbruik"),
    ("Espace Développeur", "Developer Space", "Ontwikkelaarsruimte"),
    ("Gérez votre accès API et vos abonnements d'affiliation.", "Manage your API access and affiliate subscriptions.", "Beheer uw API-toegang en affiliate-abonnementen."),
    ("Consommation de l'API", "API Consumption", "API Verbruik"),
    ("Suivez l'utilisation de vos quotas en temps réel.", "Track your quota usage in real time.", "Volg uw quotaverbruik in realtime."),
    ("Votre Clé API", "Your API Key", "Uw API-sleutel"),
    ("Plan actuel :", "Current Plan:", "Huidig Plan:"),
    ("Copier", "Copy", "Kopiëren"),
    ("Gardez cette clé secrète. Elle vous permet d'authentifier vos requêtes vers notre API.", "Keep this key secret. It allows you to authenticate your requests to our API.", "Houd deze sleutel geheim. Hiermee kunt u uw verzoeken aan onze API authenticeren."),
    ("Vous n'avez pas encore activé votre accès API.", "You have not activated your API access yet.", "U heeft uw API-toegang nog niet geactiveerd."),
    ("Générer ma clé API Free", "Generate my Free API Key", "Genereer mijn gratis API-sleutel"),
    ("Boostez votre accès", "Boost your access", "Verbeter uw toegang"),
    ("appels / jour", "calls / day", "oproepen / dag"),
    ("Données complètes", "Full data", "Volledige gegevens"),
    ("Données limitées", "Limited data", "Beperkte gegevens"),
    ("Support prioritaire", "Priority support", "Prioritaire ondersteuning"),
    ("S'abonner", "Subscribe", "Abonneren"),
    ("Choisir ce plan", "Choose this plan", "Kies dit plan"),
    ("Plan actif", "Active plan", "Actief plan"),
    ("Statistiques d'utilisation", "Usage statistics", "Gebruiksstatistieken"),
    ("Utilisation aujourd'hui", "Usage today", "Gebruik vandaag"),
    ("Votre quota est réinitialisé chaque jour à minuit.", "Your quota is reset every day at midnight.", "Uw quota wordt elke dag om middernacht gereset."),
    ("Disponibles", "Available", "Beschikbaar"),
    ("Historique récent", "Recent history", "Recente geschiedenis"),
    ("Heure", "Time", "Tijd"),
    ("Méthode", "Method", "Methode"),
    ("Réponse", "Response", "Antwoord"),
    ("Aucun appel enregistré au cours des dernières 24h.", "No calls recorded in the last 24 hours.", "Geen oproepen geregistreerd in de afgelopen 24 uur."),
    
    # Success Page
    ("Abonnement API Réussi - ThéâtrePlus", "API Subscription Successful - ThéâtrePlus", "API-abonnement geslaagd - ThéâtrePlus"),
    ("Paiement Réussi !", "Payment Successful!", "Betaling Geslaagd!"),
    ("Votre abonnement API a été mis à jour avec succès.", "Your API subscription has been successfully updated.", "Uw API-abonnement is succesvol bijgewerkt."),
    ("Bienvenue dans le plan", "Welcome to the plan", "Welkom bij het plan"),
    ("Votre accès API a été instantanément mis à niveau. Vous pouvez désormais effectuer jusqu'à", "Your API access has been instantly upgraded. You can now make up to", "Uw API-toegang is direct geüpgraded. U kunt nu maximaal"),
    ("Résumé de vos avantages :", "Summary of your benefits:", "Samenvatting van uw voordelen:"),
    ("Accès complet aux données (artistes, prix...)", "Full access to data (artists, prices...)", "Volledige toegang tot gegevens (artiesten, prijzen...)"),
    ("Accès limité aux données de base", "Limited access to basic data", "Beperkte toegang tot basisgegevens"),
    ("Retourner à l'Espace API", "Return to API Space", "Terug naar API-ruimte"),
    ("Mon Profil", "My Profile", "Mijn Profiel"),
]

def update_po(path, lang_idx):
    if not os.path.exists(path):
        return
    
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Nettoyage des anciennes entrées manuelles pour éviter les doublons
    clean_lines = []
    skip = False
    for line in lines:
        if 'msgid "Accès API"' in line or 'msgid "Abonnement API Réussi' in line:
            skip = True
        if skip and line.strip() == "":
            skip = False
            continue
        if not skip:
            clean_lines.append(line)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(clean_lines)
        for fr, en, nl in translations:
            target = en if lang_idx == 1 else nl
            f.write(f'\nmsgid "{fr}"\nmsgstr "{target}"\n')

update_po('locale/en/LC_MESSAGES/django.po', 1)
update_po('locale/nl/LC_MESSAGES/django.po', 2)
print("Files updated with success page translations")
