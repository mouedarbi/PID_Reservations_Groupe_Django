
## Date: samedi 21 mars 2026

### Progress Summary - Custom Admin Dashboard

Cette session a été consacrée à l'implémentation et à la validation du dashboard d'administration personnalisé, en veillant à ne pas modifier l'admin Django natif.

#### 1. Implémentation des vues Liste et Détail pour le dashboard personnalisé

Toutes les vues de liste (index) et de détail pour les modèles clés ont été créées et intégrées au dashboard, remplaçant les accès directs à l'admin Django par défaut pour ces fonctionnalités :
-   **Vues créées/mises à jour** : `admin_dashboard`, `admin_show_index`, `admin_representation_index`, `admin_artist_index`, `admin_type_index`, `admin_review_index`, `admin_location_index`, `admin_locality_index`, `admin_reservation_index`, `admin_reservation_detail`, `admin_user_index`, `admin_group_index`, `admin_price_index`, `admin_show_detail`.
-   **URLs configurées** : Toutes les routes correspondantes ont été ajoutées dans `reservations/urls.py` sous le préfixe `/admin-dashboard/`.
-   **Templates créés/mis à jour** : Les templates HTML (`index.html`, `detail.html`, `group_index.html`) pour chaque vue ont été développés dans `catalogue/templates/admin/`.

#### 2. Correction et Amélioration des Liens et Fonctionnalités

-   **Sidebar du dashboard (`admin.html`)** :
    -   Tous les liens de la navigation latérale ont été mis à jour pour pointer vers les vues du dashboard personnalisé, remplaçant les liens vers l'admin Django natif.
    -   Le lien "Accueil" du dashboard personnalisé pointe désormais vers `admin_dashboard`.
    -   Le lien "Détails des réservations" a été supprimé de la sidebar car il était redondant (l'accès se fait via l'icône "œil" de la liste des réservations).
-   **Gestion des Prix pour les Spectacles (`admin_show_detail`)** :
    -   La vue `admin_show_detail` a été enrichie pour permettre l'association et la désassociation dynamique de prix à un spectacle via le modèle `ShowPrice`.
    -   Le template `catalogue/templates/admin/show/detail.html` a été adapté pour inclure les formulaires d'ajout et de suppression fonctionnels.
-   **Corrections d'erreurs** :
    -   Correction d'une `NameError` (modèle `Price` non importé) dans `catalogue/views/admin_dashboard.py`.
    -   Correction d'une `IndentationError` and d'un problème de formatage dans `reservations/urls.py`.
    -   Correction d'une `ModuleNotFoundError` pour l'import de `ShowPrice` dans `admin_show_detail`.
    -   Correction d'une `NoReverseMatch` pour le lien d'édition des spectacles dans `catalogue/templates/admin/show/index.html`.

#### 3. Validation et Suivi du code

-   Chaque étape significative a été validée par un `git commit` avec un message clair.
-   Des `manage.py check` ont été exécutés régulièrement pour garantir l'intégrité du projet.
-   Toutes les modifications ont été poussées sur la branche `dev_mohamed`.

## Date: lundi 23 mars 2026

### Progress Summary - CRUD Admin Dashboard (Partie 1)

Cette session a marqué le début de l'implémentation des fonctionnalités CRUD pour le dashboard d'administration personnalisé.

#### 1. Module Artistes
- **Vues créées** : `admin_artist_detail`, `admin_artist_create`, `admin_artist_edit`.
- **Templates** : Création de `detail.html`, `create.html`, `edit.html` dans `catalogue/templates/admin/artist/`.
- **Améliorations** : Les liens de la liste pointent désormais vers le dashboard personnalisé plutôt que le front-end. Correction des tags de template Django (`else` au lieu de `else:`).
- **Validation** : Fonctionnalités de création, édition et affichage des détails testées et validées.

#### 2. Module Spectacles
- **Vues créées** : `admin_show_create`, `admin_show_edit`.
- **Templates** : Création de `create.html`, `edit.html` dans `catalogue/templates/admin/show/`.
- **Mises à jour** : Intégration des boutons "Ajouter" et "Modifier" dans l'index et la vue détaillée des spectacles.
- **Validation** : Fonctionnalités de création et édition testées et validées.

#### 3. Gestion Git
- Les changements ont été organisés en commits distincts pour chaque module sur la branche `dev_mohamed`.
- Amélioration visuelle des formulaires avec l'ajout de styles CSS spécifiques dans les templates.

### Tâches restantes pour la prochaine session

Poursuivre l'implémentation du CRUD pour les modules restants :
- **Lieux (Locations)** : Vues et templates Create/Update.
- **Localités (Localities)** : Vues et templates Create/Update.
- **Prix (Prices)** : Vues et templates Create/Update.
- **Types** : Vues et templates Create/Update.
- **Avis (Reviews)** : Vues et templates Create/Update.
- **Réservations** : Vues et templates Update.
- **Utilisateurs et Groupes** : Vues et templates Create/Update.

**Point crucial** : Implémenter la stratégie de **Soft Delete** (Suppression logique) pour l'ensemble des modèles afin de permettre une suppression sécurisée des données sans perte définitive.

## Date: samedi 28 mars 2026

### Progress Summary - CRUD Admin Dashboard (Partie 2)

Cette session a permis de finaliser l'implémentation des fonctionnalités CRUD pour l'ensemble des modules du dashboard d'administration personnalisé.

#### 1. Finalisation des Templates CRUD
- **Création des templates manquants** :
    - `representation/create.html` et `edit.html`.
    - `user/create.html` et `edit.html`.
    - `reservation/edit.html`.
- **Mise à jour des Index** : Tous les fichiers `index.html` (Artistes, Spectacles, Représentations, Lieux, Localités, Prix, Types, Avis, Réservations, Utilisateurs) ont été mis à jour pour inclure les liens fonctionnels vers les actions "Ajouter", "Modifier" et "Supprimer".

#### 2. Module Réservations
- **Formulaire créé** : `catalogue/forms/ReservationForm.py` pour permettre la modification du statut et de l'utilisateur associé à une réservation.
- **Vue créée** : `admin_reservation_edit` dans `catalogue/views/admin_dashboard.py`.
- **URL configurée** : Ajout de la route `admin_reservation_edit` dans `reservations/urls.py`.

#### 3. Intégration de la Suppression (Placeholder Soft Delete)
- Utilisation de la vue `admin_generic_delete` pour toutes les actions de suppression dans les templates index.
- Ajout de confirmations JavaScript (`onclick="return confirm(...)"`) sur tous les boutons de suppression pour éviter les erreurs accidentelles.

#### 4. Validation et Qualité
- Exécution de `manage.py check` : Aucune erreur système détectée.
- Cohérence visuelle maintenue sur l'ensemble des formulaires CRUD avec des styles CSS harmonisés.

### Prochaines étapes
- Implémenter réellement le **Soft Delete** dans les modèles (ajout du champ `is_deleted` et filtrage automatique).
- Améliorer la validation des formulaires côté client.
- Ajouter des messages de succès (Django messages framework) après chaque action CRUD.

## Roadmap : Module de Réservation & Paiement (Brainstorming du 28/03/2026)

### 1. Architecture Applicative
- **Création de l'application `cart` (ou `booking`)** : Isoler la logique de panier et de tunnel d'achat du reste du frontend.
- **Gestion du Panier** : Utilisation des **Django Sessions** pour stocker temporairement les choix de l'utilisateur (Représentation, Type de Prix, Quantité) avant l'engagement en base de données.

### 2. Évolution du Modèle de Données (Backend)
- **Table `RepresentationReservation`** :
    - Ajouter un champ `price_snapshot` (DecimalField) pour figer le prix au moment de l'achat et garantir l'intégrité comptable en cas de modification ultérieure des tarifs.
- **Création du module `Payment`** :
    - Nouveau modèle `PaymentTransaction` pour stocker les logs techniques (ID transaction, statut prestataire, réponse JSON complète).
    - Permet de dissocier la "Réservation" (objet métier) de la "Tentative de paiement" (log technique).
- **Statuts de Réservation** : Migration vers des constantes standardisées (`PENDING`, `PAID`, `CANCELED`, `FAILED`).

### 3. Workflow Frontend (Tunnel d'achat)
- **Étape 1 : Panier** -> Récapitulatif des séances choisies et calcul dynamique du total. Vérification des `available_seats` en temps réel.
- **Étape 2 : Validation** -> Transformation du panier session en objet `Reservation` avec statut `PENDING`.
- **Étape 3 : Paiement (Simulation)** -> Interface de test avec choix [Succès / Échec] pour valider le comportement du système avant l'intégration d'une API réelle (Stripe/PayPal).

## Date: lundi 6 avril 2026

### Progress Summary - Importation de Données via API Externe

Cette session a été consacrée à l'enrichissement de la base de données par l'importation de données réelles provenant d'une API publique (ODWB).

#### 1. Implémentation de la Commande de Gestion (`import_locations`)

Pour automatiser l'ajout de lieux de spectacles, une commande de gestion Django personnalisée a été créée :
-   **Fichier créé** : `catalogue/management/commands/import_locations.py`.
-   **Source des données** : API de l'Open Data Wallonie-Bruxelles (ODWB) recensant les salles de concert et théâtres.
-   **Technologie utilisée** : Bibliothèque `requests` pour les appels HTTP et `BaseCommand` de Django pour l'intégration au CLI `manage.py`.

#### 2. Logique d'Importation et Mapping des Données

Le script a été conçu pour transformer les données brutes de l'API en objets Django cohérents avec le schéma existant :
-   **Localités** : Création automatique ou récupération des objets `Locality` en utilisant le code postal et la ville fournis par l'API.
-   **Lieux (Locations)** :
    *   **Mapping des champs** : `salle` -> `designation`, `adresse` -> `address`, `site_web` -> `website`, `telephone` -> `phone`.
    *   **Génération de Slugs** : Utilisation de `slugify` pour générer des slugs uniques, avec un système de compteur incrémental pour éviter les collisions en cas de noms identiques.

#### 3. Gestion de l'Intégrité et des Doublons

Un point crucial a été d'assurer que l'importation n'interfère pas avec les données existantes des fixtures :
-   **Méthode de vérification** : Le script recherche d'abord si une salle avec la même `designation` existe déjà.
-   **Comportement** : 
    *   Si la salle existe déjà (ex: issue des fixtures JSON), elle est **mise à jour** avec les dernières informations de l'API.
    *   Si elle est nouvelle, elle est **créée**.
-   **Résultat du premier import** : 99 nouveaux lieux créés et 1 lieu mis à jour (**Espace Magh**), sans créer de doublons avec les données de démonstration initiales.

#### 4. Utilisation

La commande peut être relancée à tout moment pour synchroniser la base de données locale avec les mises à jour de l'API ODWB :
```bash
python manage.py import_locations
```

## Date: lundi 13 avril 2026

### Progress Summary - Espace Producteur & Modération Admin

Cette session a été consacrée à l'implémentation d'un workflow collaboratif entre les producteurs et l'administration pour la publication de nouveaux spectacles.

#### 1. Évolutions du Modèle de Données (Backend)

Pour supporter ce nouveau flux, plusieurs modèles ont été enrichis :
- **Modèle `Show`** : Ajout d'une relation `producer` (ForeignKey vers `User`) et d'un champ `status` (`pending`, `published`).
- **Modèle `Location`** : Ajout du champ `capacity` pour définir la jauge maximale de chaque salle.
- **Modèle `Representation`** : Ajout de `total_seats` pour garder une trace du quota initial de billets.
- **Mise à jour de l'Importer** : Le script `import_locations` récupère désormais la capacité réelle des salles via le champ `jauge_maximale` de l'API ODWB.

#### 2. Espace Producteur (Dashboard Dédié)

Création d'une interface sécurisée pour les utilisateurs du groupe `PRODUCER` :
- **Tableau de bord** : Vue synthétique des spectacles partagés avec statistiques de ventes (tickets vendus, places restantes) et état de publication.
- **Soumission de Spectacle** : Formulaire interactif permettant de proposer un spectacle (titre, durée, salle, date, heure, nombre de tickets).
- **Validation Frontend** : Intégration de JavaScript pour afficher dynamiquement la capacité de la salle sélectionnée et interdire une mise en vente supérieure à la jauge réelle.
- **Modération des Avis** : Interface permettant aux producteurs de gérer (approuver/rejeter) les critiques concernant uniquement leurs propres productions.

#### 3. Flux de Modération Administrateur

Renforcement du contrôle éditorial via le Dashboard Admin :
- **Système d'Alerte** : Ajout d'un compteur "Spectacles en attente" sur la page d'accueil de l'administration.
- **Interface de Validation** : Vue dédiée permettant à l'admin d'examiner les propositions des producteurs, de modifier les détails techniques si nécessaire, et d'affecter les tarifs (VIP, Standard, etc.).
- **Publication** : Le passage au statut `published` rend le spectacle visible et réservable pour le grand public.

#### 4. Intégration et Sécurité

- **Rôles** : Utilisation du groupe `PRODUCER` pour filtrer l'accès aux fonctionnalités et garantir qu'un producteur ne peut modifier que ses propres données.
- **Interface Utilisateur** : Distinction visuelle claire dans le profil utilisateur entre les liens "Administration" (staff) et "Espace Producteur" (group producer).

### Correctifs et Ajustements (Post-Implémentation)

- **Fix Dashboard Admin** : Résolution d'une `TemplateSyntaxError` causée par l'absence du tag `{% load i18n %}` dans le template principal du dashboard.
- **Données de Capacité** : Correction d'un bug où la capacité des salles restait à 0. Lancement d'un script de maintenance pour synchroniser les 106 lieux avec les données réelles de l'API ODWB.
- **Sécurité et Rôles** : Affinement de la visibilité des liens dans le profil utilisateur pour éviter qu'un super-administrateur ne voit le menu "Espace Producteur", clarifiant ainsi les périmètres d'action de chaque rôle.
- **Fix IntegrityError** : Résolution d'une erreur lors de l'ajout de tarifs dans le dashboard admin. Le champ `quantity_total` du modèle `ShowPrice` a été réintégré et synchronisé avec la base de données (migration faked pour correspondre à l'état réel de MySQL).
- **Fix ValueError** : Correction d'un crash dans la validation des spectacles où le système tentait de parser des dates/heures vides lors de l'ajout d'un simple tarif. La mise à jour de la séance est désormais optionnelle.
- **UI Modernisation** : Refonte visuelle de la page "Demandes Producteurs" et de l'interface d'approbation pour une coherence parfaite avec la charte graphique du nouveau dashboard administrateur.
- **Fix Persistance Approbation** : Correction d'un bug de perte de données (titre, lieu, durée) lors de l'actualisation ou de l'ajout de tarifs sur la page de validation administrateur.
- **Amélioration Modération Avis** : Affichage explicite des étoiles (notation numérique et graphique) pour le producteur lors de la modération des commentaires.
- **Support des Images (Posters)** : Ajout de la gestion du champ `poster_url` dans le flux de soumission producteur et d'approbation admin, permettant l'affichage d'images personnalisées par spectacle.
- **Logique d'affichage Frontend** : Implémentation du libellé "à partir de" pour les prix et correction du bug "Date inconnue" sur les cartes de spectacles grâce à une nouvelle propriété API `formatted_next_date`.

## Date: lundi 20 avril 2026

### Progress Summary - Système d'Upload d'Images Local

Cette session a été consacrée à la migration du système d'images des spectacles d'un modèle basé sur des URLs externes vers un système d'upload de fichiers locaux.

#### 1. Configuration de l'Environnement (Media)
- **Paramétrage Django** : Configuration de `MEDIA_URL` et `MEDIA_ROOT` dans `reservations/settings.py` pour définir l'emplacement de stockage des fichiers téléchargés.
- **Serveur de Media** : Ajout des routes statiques pour les fichiers média dans `reservations/urls.py` afin de permettre l'affichage des images en mode développement.

#### 2. Évolution du Modèle Show
- **Migration ImageField** : Remplacement du champ `poster_url` (CharField) par un champ `poster` de type `ImageField` avec stockage dans le dossier `/posters/`.
- **Synchronisation API** : Mise à jour de `ShowSerializer` pour inclure le champ `poster` et generer des URLs d'images valides pour le frontend.

#### 3. Workflow de Soumission (Producteurs)
- **Upload Direct** : Mise à jour des formulaires `prod_submit_show` et `prod_edit_show` pour supporter l'envoi de fichiers binaires depuis l'ordinateur du producteur (ajout de `enctype="multipart/form-data"`).
- **Traitement des Fichiers** : Modification des vues du dashboard producteur pour intercepter et sauvegarder les fichiers via `request.FILES`.

#### 4. Interface de Validation (Administration)
- **Lecture seule** : Modification de la vue d'approbation admin pour afficher la photo téléchargée par le producteur sans permettre à l'administrateur de la modifier ou de la supprimer, garantissant l'intégrité de la proposition visuelle originale.

#### 5. Mise à jour Frontend
- **Affichage Dynamique** : Adaptation de tous les templates clients (`home.html`, `show_list.html`, `show_detail.html`) pour utiliser `show.poster.url` avec un système de fallback (image par défaut) si aucun poster n'est disponible.

## Date: mardi 21 avril 2026

### Progress Summary - Système d'Épinglage des Avis (Reviews)

Cette session a été consacrée à l'ajout d'une fonctionnalité permettant aux producteurs de mettre en avant certains avis spectateurs sur la page de leurs spectacles.

#### 1. Évolution du Modèle Review
- **Nouveau champ** : Ajout d'un champ boolean `is_pinned` (défaut: `False`) au modèle `Review`.
- **Migration** : Création et application de la migration `0040_review_is_pinned.py`.

#### 2. Interface de Modération (Producteur)
- **Gestion de l'épinglage** : Ajout d'une vue `pin_review` permettant aux producteurs de toggler (activer/désactiver) l'état d'épinglage d'un avis.
- **Sécurité** : Mise en place d'une vérification stricte garantissant qu'un producteur ne peut épingler que les avis liés à ses propres spectacles.
- **Amélioration UI** : Mise à jour du template `moderate_reviews.html` avec un nouveau bouton d'épingle. Le style a été affiné pour offrir un retour visuel clair (fond jaune ambre et icône remplie) lorsqu'un avis est épinglé.

#### 3. Affichage Frontend (Détail du Spectacle)
- **Priorisation** : Modification de la logique d'affichage dans `show_detail.html` pour que les avis épinglés apparaissent systématiquement en haut de la liste (tri par `is_pinned` décroissant).
- **Mise en évidence** : Les avis épinglés bénéficient désormais d'une bordure ambre, d'un fond légèrement teinté et d'un badge visuel **"Épinglé"** avec une icône de punaise à côté du nom de l'utilisateur.
- **Compatibilité API** : Mise à jour du `ReviewSerializer` dans `api/serializers/shows.py` pour inclure le champ `is_pinned`, assurant ainsi la persistance de l'information lors du chargement dynamique des données.

## Date: mercredi 29 avril 2026

### Progress Summary - Demandes pour Devenir Producteur

Cette session a été consacrée à la mise en place d'un système permettant aux utilisateurs classiques de postuler pour devenir producteurs.

#### 1. Système de Demande (Frontend)
- **Point d'entrée** : Ajout d'un lien "Devenir Producteur ?" dans la barre de navigation, visible uniquement pour les utilisateurs connectés non-staff et non-producteurs.
- **Formulaire Utilisateur** : Création de la page de soumission (`become_producer.html`) et du formulaire `ProducerRequestForm` permettant aux candidats de saisir leurs informations (Nom, Prénom, Email, Téléphone, Adresse, Présentation, Motivation).
- **Protection anti-spam** : Une fois la demande soumise, le système bloque la création d'une nouvelle demande et affiche un message d'attente à l'utilisateur.

#### 2. Modèle de Données (Backend)
- **Modèle `ProducerRequest`** : Création du modèle pour stocker les demandes avec des champs dédiés (first_name, last_name, email, phone, address, presentation, motivation) et un système de statut (`pending`, `approved`, `rejected`).
- **Liaisons** : Le modèle est relié à l'utilisateur Django (`User`).

#### 3. Modération par l'Administrateur
- **Dashboard Admin** : Intégration d'une nouvelle section "Producteurs Juniors" dans le menu de gauche.
- **Vue d'examen** : Mise à jour visuelle du template `producer_request/pending.html` pour correspondre à l'esthétique moderne du dashboard admin (mode sombre, couleurs, cartes, tableaux structurés).
- **Interface Modale** : L'examen d'une demande ouvre désormais une fenêtre modale (Modal) claire affichant toutes les informations du candidat (présentation, motivation, coordonnées) sans quitter la liste.
- **Action de validation** : L'admin peut "Refuser" ou "Accepter". En cas d'acceptation, l'utilisateur est automatiquement ajouté au groupe `PRODUCER` et gagne accès à son propre Espace Producteur.

#### 4. Améliorations de l'UI/UX du Dashboard Administrateur
- **Simplification de la Sidebar** : Remplacement des menus déroulants redondants ("Vue d'ensemble > Accueil", "Réservations > Réservations", "Utilisateurs > Utilisateurs") par des liens directs et clairs pour améliorer la navigation.
- **Menu Profil Admin (En-tête)** : L'icône de profil en haut à droite est désormais cliquable et fonctionnelle. Elle affiche un menu contextuel permettant de "Revenir au site" (accès direct au front-end tout en restant connecté) et de "Se déconnecter" (redirection propre vers l'accueil via le système Django).
- **Notifications** : L'icône des notifications a été rendue interactive et affiche désormais un état vide élégant ("Vous n'avez aucune notification pour l'instant") en l'absence d'alertes.

#### 5. Optimisations et Correctifs
- **Transition de Rôle** : Lors de l'approbation d'un producteur, l'utilisateur est maintenant correctement basculé du groupe "MEMBER" vers le groupe "PRODUCER", assurant la mise à jour immédiate de ses droits et de son interface.
- **Performance et Stabilité** : Suppression de scripts de rechargement inutiles qui provoquaient des ralentissements sur certaines pages.
- **Correctifs d'Interactivity** : Résolution des conflits d'IDs dans le JavaScript pour garantir le bon fonctionnement des menus déroulants (profil et notifications) sur l'ensemble du dashboard.

## Date: lundi 4 mai 2026

### Progress Summary - Système de Notifications Admin & Correctifs

Cette session a été consacrée à l'implémentation complète d'un système de notifications pour le dashboard d'administration, permettant un suivi en temps réel des activités critiques.

#### 1. Système de Notifications (Backend)
- **Modèle Notification** : Création du modèle pour stocker les alertes avec types catégorisés (new_user, producer_request, new_show), messages formatés HTML et liens de redirection dynamiques.
- **Automatisation via Signals** : Implémentation de triggers automatiques dans catalogue/signals.py qui génèrent une notification admin lors de :
    - L'inscription d'un nouvel utilisateur.
    - La soumission d'une demande pour devenir producteur.
    - La soumission d'un nouveau spectacle par un producteur pour approbation.
- **Context Processor** : Création de admin_notifications pour injecter les notifications non lues et le compteur global dans tous les templates du dashboard admin.

#### 2. Interface Utilisateur & Interactivité (Admin Dashboard)
- **Topbar Dynamique** : Mise à jour du bouton cloche dans admin.html pour afficher un badge rouge avec le nombre exact de notifications non lues et un menu déroulant affichant les 10 alertes les plus récentes.
- **Gestion des Lectures** : Implémentation d'une vue de redirection qui marque une notification comme lue avant d'envoyer l'administrateur vers la page concernée (ex: fiche du spectacle à approuver).
- **Historique Complet** : Création d'une page dédiée admin_notifications avec pagination pour consulter l'ensemble des notifications passées.
- **Action Groupée** : Ajout d'une fonctionnalité "Tout marquer comme lu" pour une gestion rapide du flux d'alertes.

#### 3. Correctifs de Base de Données
- **Migration Manquante** : Résolution d'une `ProgrammingError (1146)` causée par l'absence de la table `catalogue_notification`. 
- **Actions** : Génération et application de la migration `0046_notification.py` pour synchroniser le schéma MySQL avec le nouveau modèle.

#### 4. Intégration Git
- Organisation des changements en commits structurés.
- **Push Final** : Synchronisation de l'ensemble du travail sur le dépôt distant.

