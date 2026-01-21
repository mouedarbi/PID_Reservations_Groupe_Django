# 🧾 Journal de Bord – Mapping et Relations Complexes
**Projet :** Réservations (PID)  
**Étudiant :** Mohamed Ouedarbi  
**Framework :** Django 5 + MySQL  
**Période :** Novembre 2025  

---

## 📅 27/11/2025 – Modélisation des données et correction des fixtures

**Contexte :**
- Poursuite du projet en suivant le `Roadmap-Django5_Mapping.txt`.
- Objectif : implémenter les modèles `Representation`, `Review`, et les relations `ManyToMany` entre `Artist` et `Type`.

---

### 🧩 Erreur 1 – `DataError` à la migration

**Message :**  
`django.db.utils.DataError: (1264, "Out of range value for column 'created_in' at row 1")`  

**Cause :**  
La base de données MySQL contenait des données invalides pour la colonne `created_in` de la table `shows`, ce qui empêchait l'application de nouvelles migrations. Mon hypothèse initiale d'une base de données SQLite était incorrecte.

**Résolution :**  
Utilisation de la commande `python manage.py flush` pour vider complètement la base de données MySQL, suivie de `python manage.py migrate` pour reconstruire le schéma.

**Statut :** ✅ Résolu  

---

### 🧩 Erreur 2 – Incohérences dans les fixtures (`loaddata`)

Plusieurs erreurs `IntegrityError` et `DeserializationError` sont survenues lors du chargement des fixtures (`loaddata`).

**Causes et résolutions :**
1.  **`reservations.json`** : Une réservation faisait référence à un utilisateur "Jordan" qui n'existait pas dans `auth_user.json`.
    - **Correction :** Remplacement de "Jordan" par "anna" dans `reservations.json`.
2.  **`locations.json`** : Les spectacles dans `shows.json` référençaient des lieux avec une clé naturelle `(slug, website)`, mais le champ `website` était `null` dans `locations.json`, provoquant un `Location.DoesNotExist`.
    - **Correction :** Ajout des URLs manquantes pour "espace-delvaux-la-venerie" et "la-samaritaine" dans `locations.json`.
3.  **`artist_type.json`** : Erreur `LookupError: App 'catalogue' doesn't have a 'artist_type' model` car le fixture essayait de charger des données dans une table de jointure auto-générée, qui n'est pas un modèle Django.
    - **Correction (après refactoring) :** Le nom du modèle dans le fixture a été corrigé pour `catalogue.ArtistType` (avec une majuscule).
4.  **`artist_type.json` (suite)** : Erreur `ValidationError: value must be an integer` car le modèle `Artist` n'avait plus de `natural_key` pour résoudre `['Daniel', 'Marcelin']`.
    - **Correction :** Ré-ajout du `ArtistManager` et de la méthode `natural_key` au modèle `Artist`.

**Statut :** ✅ Résolu  

---

### ✅ Actions réalisées

1.  **Modèle `Representation` :**
    - Création du modèle `catalogue/models/representation.py`.
    - Ajout du `ShowManager` et de la `natural_key` au modèle `Show`.
    - Création et application des migrations (`0011_representation`, `0012_show_unique_slug_created_in`).
    - Création et chargement de la fixture `representations.json`.

2.  **Modèle `Review` :**
    - Création du modèle `catalogue/models/review.py`.
    - Création et application de la migration (`0013_review`).
    - Création et chargement de la fixture `reviews.json`.

3.  **Relation `Artist` <-> `Type` (`ManyToMany`) :**
    - **Étape 1 (Erreur documentée) :** Ajout du champ `ManyToManyField` à `Artist`, ajout des clés naturelles, et tentative de chargement de `artist_type.json` qui a échoué. Un commit a été fait à cette étape pour documenter l'erreur, comme demandé.
    - **Étape 2 (Refactoring) :**
        - Suppression du `ManyToManyField` du modèle `Artist`.
        - Création des modèles intermédiaires `ArtistType` et `ArtistTypeShow`.
        - Modification du modèle `Show` pour utiliser la nouvelle table de jointure.
        - Application de toutes les migrations correspondantes (`0014` à `0020`).
        - Correction de la fixture `artist_type.json` et chargement réussi.

4.  **Gestion Git :**
    - Création de commits distincts pour les modules `Representation` et `Review`.
    - Ajout des fichiers de documentation (`gemini.md`, `Roadmap-*.txt`, `database_structure.txt`) au `.gitignore` et suppression de l'historique Git.
    - Push de toutes les modifications sur la branche `dev_mohamed`.

---

### ✅ Vues, Templates et Routes (Location, Show, Representation)

**Contexte :**
- Après la modélisation des données, implémentation des composants front-end pour visualiser les données.

**Actions réalisées :**
1.  **Routes URL :** Ajout des routes `location-index`, `location-show`, `show-index`, `show-show`, `representation-index`, `representation-show` à `catalogue/urls.py`.
2.  **Vues :**
    - Création de `catalogue/views/location.py` (fonctions `index` et `show`).
    - Création de `catalogue/views/show_.py` (fonctions `index` et `show`).
    - Création de `catalogue/views/representation.py` (fonctions `index` et `show`).
    - Mise à jour de `catalogue/views/__init__.py` pour importer les nouvelles vues.
3.  **Templates :**
    - Création des répertoires `catalogue/templates/location`, `catalogue/templates/show`, `catalogue/templates/representation`.
    - Création de `index.html` et `show.html` pour chaque répertoire de template.
    - Correction d'une erreur de déplacement de `location/show.html` vers le répertoire `show`, puis remise à sa place correcte.
4.  **Menu de navigation :** Ajout des liens de navigation vers les vues `index` de `Type`, `Locality`, `Price`, `Location`, `Show`, et `Representation` dans `catalogue/templates/layouts/base.html`.
5.  **Mise à jour des templates `artist/show.html` et `type/show.html`:** Adaptation de l'affichage des relations ManyToMany pour utiliser les modèles intermédiaires (`artist.a_artistTypes.all` et `type.t_artistTypes.all`).

**Statut :** ✅ Complet

---

## ✅ État final du projet (27/11/2025)
- Modèles `Representation`, `Review`, `ArtistType` et `ArtistTypeShow` implémentés et migrés. ✔️  
- Base de données MySQL nettoyée et entièrement peuplée avec toutes les fixtures corrigées. ✔️  
- Le projet est maintenant à jour avec la roadmap jusqu'à la fin de la modélisation des relations complexes. ✔️  
- L'historique Git est propre et les fichiers de documentation sont ignorés. ✔️  
- Toutes les vues, templates et routes pour les modèles implémentés sont en place et fonctionnels. ✔️  

---
## 📅 30/11/2025 – CRUD pour le modèle Review

**Contexte :**
- Finalisation des fonctionnalités CRUD pour les modèles restants.

**Actions réalisées :**
1.  **Formulaire :** Création de `catalogue/forms/ReviewForm.py` pour gérer la création et la modification des critiques.
2.  **Vues :** Implémentation des vues `index`, `show`, `create`, `edit`, et `delete` dans `catalogue/views/review.py`, avec gestion des permissions.
3.  **Templates :** Création des templates `index.html`, `show.html`, `create.html`, et `edit.html` dans `catalogue/templates/review/`.
4.  **Routes URL :** Ajout des routes correspondantes dans `catalogue/urls.py`.
5.  **Menu de navigation :** Ajout d'un lien vers la liste des critiques dans `catalogue/templates/layouts/base.html`.

**Statut :** ✅ Complet

---

## ✅ État final du projet (30/11/2025)
- Modèles `Representation`, `Review`, `ArtistType` et `ArtistTypeShow` implémentés et migrés. ✔️  
- Base de données MySQL nettoyée et entièrement peuplée avec toutes les fixtures corrigées. ✔️  
- Le projet est maintenant à jour avec la roadmap jusqu'à la fin de la modélisation des relations complexes. ✔️  
- L'historique Git est propre et les fichiers de documentation sont ignorés. ✔️  
- Toutes les vues, templates et routes pour les modèles implémentés sont en place et fonctionnels. ✔️
- CRUD complet pour le modèle `Review`. ✔️  
- CRUD complet pour le modèle `Locality`. ✔️
- CRUD complet pour le modèle `Location`. ✔️
- CRUD complet pour le modèle `Price`. ✔️
- CRUD complet pour le modèle `Representation`. ✔️
- CRUD complet pour le modèle `Show`. ✔️
- CRUD complet pour le modèle `Type`. ✔️
- Gestion des permissions et droits d'accès affinée et corrigée. ✔️

---

**Auteur :**  
Mohamed Ouedarbi – Bachelier en Informatique de gestion  
📅 Dernière mise à jour : 30/11/2025

---
## 📅 30/11/2025 – CRUD pour le modèle Locality

**Contexte :**
- Implémentation des fonctionnalités CRUD pour le modèle `Locality`.

**Actions réalisées :**
1.  **Formulaire :** Création de `catalogue/forms/LocalityForm.py`.
2.  **Vues :** Ajout des vues `create`, `edit`, et `delete` dans `catalogue/views/locality.py`, avec gestion des permissions.
3.  **Templates :** Création de `catalogue/templates/locality/create.html` et `catalogue/templates/locality/edit.html`.
4.  **Routes URL :** Ajout des routes correspondantes dans `catalogue/urls.py`.
5.  **Templates `index` et `show` :** Mise à jour des templates `locality/index.html` et `locality/show.html` pour inclure des liens vers les actions CRUD.

**Statut :** ✅ Complet

---
## 📅 30/11/2025 – CRUD pour le modèle Location

**Contexte :**
- Implémentation des fonctionnalités CRUD pour le modèle `Location`.

**Actions réalisées :**
1.  **Formulaire :** Création de `catalogue/forms/LocationForm.py`.
2.  **Vues :** Ajout des vues `create`, `edit`, et `delete` dans `catalogue/views/location.py`, avec gestion des permissions.
3.  **Templates :** Création de `catalogue/templates/location/create.html` et `catalogue/templates/location/edit.html`.
4.  **Routes URL :** Ajout des routes correspondantes dans `catalogue/urls.py`.
5.  **Templates `index` et `show` :** Mise à jour des templates `location/index.html` et `location/show.html` pour inclure des liens vers les actions CRUD.

**Statut :** ✅ Complet

---
## 📅 30/11/2025 – CRUD pour le modèle Price

**Contexte :**
- Implémentation des fonctionnalités CRUD pour le modèle `Price`.

**Actions réalisées :**
1.  **Formulaire :** Création de `catalogue/forms/PriceForm.py`.
2.  **Vues :** Ajout des vues `create`, `edit`, et `delete` dans `catalogue/views/price.py`, avec gestion des permissions.
3.  **Templates :** Création de `catalogue/templates/price/create.html` et `catalogue/templates/price/edit.html`.
4.  **Routes URL :** Ajout des routes correspondantes dans `catalogue/urls.py`.
5.  **Templates `index` et `show` :** Mise à jour des templates `price/index.html` et `price/show.html` pour inclure des liens vers les actions CRUD.

**Statut :** ✅ Complet

---
## 📅 30/11/2025 – CRUD pour le modèle Representation

**Contexte :**
- Implémentation des fonctionnalités CRUD pour le modèle `Representation`.

**Actions réalisées :**
1.  **Formulaire :** Création de `catalogue/forms/RepresentationForm.py`.
2.  **Vues :** Ajout des vues `create`, `edit`, et `delete` dans `catalogue/views/representation.py`, avec gestion des permissions.
3.  **Templates :** Création de `catalogue/templates/representation/create.html` et `catalogue/templates/representation/edit.html`.
4.  **Routes URL :** Ajout des routes correspondantes dans `catalogue/urls.py`.
5.  **Templates `index` et `show` :** Mise à jour des templates `representation/index.html` et `representation/show.html` pour inclure des liens vers les actions CRUD.

**Statut :** ✅ Complet

---
## 📅 30/11/2025 – CRUD pour le modèle Show

**Contexte :**
- Implémentation des fonctionnalités CRUD pour le modèle `Show`.

**Actions réalisées :**
1.  **Formulaire :** Création de `catalogue/forms/ShowForm.py`.
2.  **Vues :** Ajout des vues `create`, `edit`, et `delete` dans `catalogue/views/show_.py`, avec gestion des permissions.
3.  **Templates :** Création de `catalogue/templates/show/create.html` et `catalogue/templates/show/edit.html`.
4.  **Routes URL :** Ajout des routes correspondantes dans `catalogue/urls.py`.
5.  **Templates `index` et `show` :** Mise à jour des templates `show/index.html` et `show/show.html` pour inclure des liens vers les actions CRUD.

**Statut :** ✅ Complet

---
## 📅 30/11/2025 – CRUD pour le modèle Type

**Contexte :**
- Implémentation des fonctionnalités CRUD pour le modèle `Type`.

**Actions réalisées :**
1.  **Formulaire :** Création de `catalogue/forms/TypeForm.py`.
2.  **Vues :** Ajout des vues `create`, `edit`, et `delete` dans `catalogue/views/type.py`, avec gestion des permissions.
3.  **Templates :** Création de `catalogue/templates/type/create.html` and `catalogue/templates/type/edit.html`.
4.  **Routes URL :** Ajout des routes correspondantes dans `catalogue/urls.py`.
5.  **Templates `index` et `show` :** Mise à jour des templates `type/index.html` et `type/show.html` pour inclure des liens vers les actions CRUD.

**Statut :** ✅ Complet

---

**Auteur :**  
Mohamed Ouedarbi – Bachelier en Informatique de gestion  
📅 Dernière mise à jour : 30/11/2025

---
## 📅 14/01/2026 – Organisation et Structuration des Issues GitHub

**Contexte :**
- Mise en place d'une organisation claire des tâches du projet via les issues GitHub.

**Actions réalisées :**
1.  **Création du système de labellisation :** Mise en place de labels catégorisés pour les Composants (`C:`), les Applications Django (`A:`), les Types de tâches (`T:`), et les Itérations du projet (`I:`), basés sur le `README.md`.
2.  **Labellisation des issues existantes :** Les 14 issues GitHub préexistantes ont été analysées et labellisées selon le nouveau système.
3.  **Création des nouvelles issues :** 59 nouvelles issues GitHub ont été créées à partir de la liste exhaustive des fonctionnalités fournies par l'utilisateur, chacune avec un titre descriptif et les labels appropriés.

**Statut :** ✅ Complet

---

**Auteur :**  
Mohamed Ouedarbi – Bachelier en Informatique de gestion  
📅 Dernière mise à jour : 14/01/2026