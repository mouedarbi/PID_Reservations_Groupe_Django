
import re
import os

def translate_po(file_path, translations):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    for msgid, msgstr in translations.items():
        # Handle multi-line msgid if necessary
        pattern = re.compile(f'msgid "{re.escape(msgid)}"\nmsgstr ""')
        if pattern.search(content):
            content = pattern.sub(f'msgid "{msgid}"\nmsgstr "{msgstr}"', content)
        else:
            # Try with fuzzy marker
            pattern_fuzzy = re.compile(f'#, fuzzy\n#\\| msgid ".*?"\nmsgid "{re.escape(msgid)}"\nmsgstr ".*?"')
            if pattern_fuzzy.search(content):
                 content = pattern_fuzzy.sub(f'msgid "{msgid}"\nmsgstr "{msgstr}"', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

en_translations = {
    "Conditions Générales - ThéâtrePlus": "General Terms and Conditions - ThéâtrePlus",
    "Conditions": "Terms",
    "Mentions légales, CGV et Protection des données": "Legal notice, T&C and Data Protection",
    "Mentions Légales": "Legal Notice",
    "Éditeur du site": "Site Publisher",
    "Siège social": "Registered Office",
    "Vente de Tickets en Ligne": "Online Ticket Sales",
    "Conformément au Code de droit économique belge :": "In accordance with the Belgian Code of Economic Law:",
    "Absence de droit de rétractation": "No right of withdrawal",
    "En vertu de l'article VI.53, 12° du Code de droit économique, le droit de rétractation de 14 jours ne s'applique pas aux prestations de services de loisirs devant être fournies à une date déterminée.": "According to Article VI.53, 12° of the Code of Economic Law, the 14-day right of withdrawal does not apply to leisure services to be provided on a specific date.",
    "Validité": "Validity",
    "Les tickets ne sont valables que pour la représentation, la date et l'heure indiquées.": "Tickets are only valid for the specified performance, date, and time.",
    "Remboursement": "Refund",
    "Sauf en cas d'annulation ou de report par l'organisateur, les tickets ne sont ni échangés ni remboursés.": "Except in case of cancellation or postponement by the organizer, tickets are neither exchanged nor refunded.",
    "Protection des Données (GDPR)": "Data Protection (GDPR)",
    "Conformément au Règlement Général sur la Protection des Données (UE 2016/679) :": "In accordance with the General Data Protection Regulation (EU 2016/679):",
    "Finalité": "Purpose",
    "Vos données sont collectées pour la gestion des réservations et l'accès aux services de l'API.": "Your data is collected for booking management and access to API services.",
    "Rétention des données": "Data retention",
    "Les données relatives à votre compte sont conservées tant que votre compte est actif. En cas d'inactivité prolongée de 3 ans, vos données personnelles seront anonymisées ou supprimées.": "Data related to your account is kept as long as your account is active. In case of prolonged inactivity of 3 years, your personal data will be anonymized or deleted.",
    "Vos droits": "Your rights",
    "Vous disposez d'un droit d'accès, de rectification et de suppression ('droit à l'oubli') de vos données.": "You have a right to access, rectification, and deletion ('right to be forgotten') of your data.",
    "Suppression de compte": "Account deletion",
    "Vous pouvez demander la suppression de votre compte à tout moment via votre profil ou par e-mail. Cette action est irréversible et entraîne la suppression de vos données personnelles, sauf obligation légale de conservation (ex: facturation).": "You can request the deletion of your account at any time via your profile or by email. This action is irreversible and leads to the deletion of your personal data, except for legal retention obligations (e.g., billing).",
    "Responsabilité": "Liability",
    "ThéâtrePlus agit en tant qu'intermédiaire entre les producteurs de spectacles et les spectateurs. La responsabilité de la tenue du spectacle incombe exclusivement au producteur mentionné sur la fiche du spectacle.": "ThéâtrePlus acts as an intermediary between show producers and spectators. The responsibility for the performance lies exclusively with the producer mentioned on the show sheet.",
    "Dernière mise à jour": "Last updated",
    "FAQ - Foire Aux Questions - ThéâtrePlus": "FAQ - Frequently Asked Questions - ThéâtrePlus",
    "FAQ": "FAQ",
    "Réponses à vos questions les plus fréquentes": "Answers to your most frequently asked questions",
    "Le Site": "The Site",
    "Qu'est-ce que ThéâtrePlus ?": "What is ThéâtrePlus?",
    "ThéâtrePlus est une plateforme de réservation en ligne dédiée aux arts de la scène en Belgique, permettant de découvrir des spectacles et de réserver vos places facilement.": "ThéâtrePlus is an online booking platform dedicated to the performing arts in Belgium, allowing you to discover shows and book your seats easily.",
    "Comment créer un compte ?": "How to create an account?",
    "Cliquez sur le bouton 'Connexion' en haut à droite, puis sélectionnez 'Créer un compte'. Remplissez le formulaire et vous pourrez commencer à réserver.": "Click on the 'Login' button at the top right, then select 'Create an account'. Fill out the form and you can start booking.",
    "Réservations": "Bookings",
    "Comment réserver un ticket ?": "How to book a ticket?",
    "Choisissez un spectacle, sélectionnez une représentation disponible, ajoutez les places au panier et procédez au paiement sécurisé via Stripe.": "Choose a show, select an available performance, add the seats to your cart, and proceed to secure payment via Stripe.",
    "Puis-je annuler ma réservation ?": "Can I cancel my reservation?",
    "Conformément à nos conditions générales, les tickets pour des événements à date fixe ne sont pas remboursables, sauf en cas d'annulation de l'organisateur.": "In accordance with our general terms and conditions, tickets for fixed-date events are non-refundable, except in case of cancellation by the organizer.",
    "Paiement & Support": "Payment & Support",
    "Quels sont les modes de paiement acceptés ?": "What payment methods are accepted?",
    "Nous acceptons les paiements par carte bancaire (Visa, Mastercard, Bancontact) via la plateforme sécurisée Stripe.": "We accept payments by credit card (Visa, Mastercard, Bancontact) via the secure Stripe platform.",
    "Que faire si je ne reçois pas mon ticket par e-mail ?": "What if I don't receive my ticket by email?",
    "Vérifiez d'abord votre dossier 'Indésirables'. Vous pouvez également retrouver tous vos tickets à tout moment dans votre espace profil sur le site.": "First check your 'Spam' folder. You can also find all your tickets at any time in your profile area on the site."
}

nl_translations = {
    "Conditions Générales - ThéâtrePlus": "Algemene Voorwaarden - ThéâtrePlus",
    "Conditions": "Voorwaarden",
    "Mentions légales, CGV et Protection des données": "Juridische informatie, AV and Gegevensbescherming",
    "Mentions Légales": "Juridische Informatie",
    "Éditeur du site": "Site Uitgever",
    "Siège social": "Maatschappelijke Zetel",
    "Vente de Tickets en Ligne": "Online Ticketverkoop",
    "Conformément au Code de droit économique belge :": "In overeenstemming met het Belgisch Wetboek van Economisch Recht:",
    "Absence de droit de rétractation": "Geen herroepingsrecht",
    "En vertu de l'article VI.53, 12° du Code de droit économique, le droit de rétractation de 14 jours ne s'applique pas aux prestations de services de loisirs devant être fournies à une date déterminée.": "Krachtens artikel VI.53, 12° van het Wetboek van Economisch Recht is het herroepingsrecht van 14 dagen niet van toepassing op vrijetijdsdiensten die op een bepaalde datum moeten worden verleend.",
    "Validité": "Geldigheid",
    "Les tickets ne sont valables que pour la représentation, la date et l'heure indiquées.": "Tickets zijn alleen geldig voor de vermelde voorstelling, datum en tijd.",
    "Remboursement": "Terugbetaling",
    "Sauf en cas d'annulation ou de report par l'organisateur, les tickets ne sont ni échangés ni remboursés.": "Behalve in geval van annulering of uitstel door de organisator, worden tickets niet geruild of terugbetaald.",
    "Protection des Données (GDPR)": "Gegevensbescherming (GDPR)",
    "Conformément au Règlement Général sur la Protection des Données (UE 2016/679) :": "In overeenstemming met de Algemene Verordening Gegevensbescherming (EU 2016/679):",
    "Finalité": "Doeleinde",
    "Vos données sont collectées pour la gestion des réservations et l'accès aux services de l'API.": "Uw gegevens worden verzameld voor boekingsbeheer and toegang tot API-diensten.",
    "Rétention des données": "Gegevensbewaring",
    "Les données relatives à votre compte sont conservées tant que votre compte est actif. En cas d'inactivité prolongée de 3 ans, vos données personnelles seront anonymisées ou supprimées.": "Gegevens met betrekking tot uw account worden bewaard zolang uw account actief is. In geval van langdurige inactiviteit van 3 jaar worden uw persoonlijke gegevens geanonimiseerd of verwijderd.",
    "Vos droits": "Uw rechten",
    "Vous disposez d'un droit d'accès, de rectification et de suppression ('droit à l'oubli') de vos données.": "U heeft recht op inzage, rectificatie and verwijdering ('recht om vergeten te worden') van uw gegevens.",
    "Suppression de compte": "Account verwijderen",
    "Vous pouvez demander la suppression de votre compte à tout moment via votre profil ou par e-mail. Cette action est irréversible et entraîne la suppression de vos données personnelles, sauf obligation légale de conservation (ex: facturation).": "U kunt op elk moment via uw profiel of per e-mail verzoeken om verwijdering van uw account. Deze actie is onomkeerbaar and leidt tot de verwijdering van uw persoonlijke gegevens, behalve voor wettelijke bewaarplichten (bijv. facturering).",
    "Responsabilité": "Aansprakelijkheid",
    "ThéâtrePlus agit en tant qu'intermédiaire entre les producteurs de spectacles et les spectateurs. La responsabilité de la tenue du spectacle incombe exclusivement au producteur mentionné sur la fiche du spectacle.": "ThéâtrePlus treedt op als tussenpersoon tussen producenten and toeschouwers. De verantwoordelijkheid voor de voorstelling ligt uitsluitend bij de producent vermeld op de showfiche.",
    "Dernière mise à jour": "Laatst bijgewerkt",
    "FAQ - Foire Aux Questions - ThéâtrePlus": "FAQ - Veelgestelde Vragen - ThéâtrePlus",
    "FAQ": "FAQ",
    "Réponses à vos questions les plus fréquentes": "Antwoorden op uw meest gestelde vragen",
    "Le Site": "De Website",
    "Qu'est-ce que ThéâtrePlus ?": "Wat is ThéâtrePlus?",
    "ThéâtrePlus est une plateforme de réservation en ligne dédiée aux arts de la scène en Belgique, permettant de découvrir des spectacles et de réserver vos places facilement.": "ThéâtrePlus is een online boekingsplatform gewijd aan de podiumkunsten in België, waarmee u shows kunt ontdekken en eenvoudig uw plaatsen kunt reserveren.",
    "Comment créer un compte ?": "Hoe maak ik een account aan?",
    "Cliquez sur le bouton 'Inloggen' rechtsboven en selecteer vervolgens 'Account aanmaken'. Vul het formulier in en u kunt beginnen met boeken.": "Klik op de knop 'Inloggen' rechtsboven en selecteer vervolgens 'Account aanmaken'. Vul het formulier in en u kunt beginnen met boeken.",
    "Réservations": "Boekingen",
    "Comment réserver un ticket ?": "Hoe reserveer ik een ticket?",
    "Choisissez un spectacle, sélectionnez une représentation disponible, ajoutez les places au panier et procédez au paiement sécurisé via Stripe.": "Kies een show, selecteer een beschikbare voorstelling, voeg de plaatsen toe aan uw winkelwagentje en ga over tot veilige betaling via Stripe.",
    "Puis-je annuler ma réservation ?": "Kan ik mijn reservering annuleren?",
    "Conformément à nos conditions générales, les tickets pour des événements à date fixe ne sont pas remboursables, sauf en cas d'annulation de l'organisateur.": "In overeenstemming met onze algemene voorwaarden zijn tickets voor evenementen op een vaste datum niet restitueerbaar, behalve in geval van annulering door de organisator.",
    "Paiement & Support": "Betaling & Ondersteuning",
    "Quels sont les modes de paiement acceptés ?": "Welke betaalmethoden worden geaccepteerd?",
    "Nous acceptons les paiements par carte bancaire (Visa, Mastercard, Bancontact) via la plateforme sécurisée Stripe.": "Wij accepteren betalingen met bankkaart (Visa, Mastercard, Bancontact) via het beveiligde Stripe-platform.",
    "Que faire si je ne reçois pas mon ticket par e-mail ?": "Wat moet ik doen als ik mijn ticket niet per e-mail ontvang?",
    "Vérifiez d'abord votre dossier 'Indésirables'. Vous pouvez également retrouver tous vos tickets à tout moment dans votre espace profil sur le site.": "Controleer eerst uw map 'Ongewenste e-mail'. U kunt al uw tickets ook op elk gewenst moment terugvinden in uw profielgedeelte op de website."
}

translate_po('locale/en/LC_MESSAGES/django.po', en_translations)
translate_po('locale/nl/LC_MESSAGES/django.po', nl_translations)
print("Translations updated successfully.")
