# Projet Réservations – Django 5

## Équipe de développement

- **Mohamed Ouedarbi**
- **Mpindu Mukandila Jean-Paul**
- **YALAOUI Ghiles**
- **Slavic Veaceslav Lisa**
- _(+ ajouter les autres membres du groupe)_

---

## Description du projet

L’application **Projet Réservations** permet de gérer les réservations de spectacles pour une société de production.
Elle comprend :

- un **catalogue de spectacles**, artistes et lieux de représentation,
- un système de **réservations en ligne**,
- un **back-office administrateur** pour gérer les contenus,
- une **API RESTful** destinée aux affiliés,
- et une future **interface front-end ReactJS** pour le public.

Ce projet s’inscrit dans le cadre du **PID (Projet d’Intégration et Développement)** du Bachelier en Informatique de gestion.
Il fait suite au _Starter Kit Django 5_ (Itération 2 du PID).

---

## Objectifs pédagogiques

- Apprendre à structurer un projet Django complet.
- Travailler collaborativement via GitHub (versioning).
- Comprendre le mapping ORM, la gestion CRUD, l’authentification et les APIs.
- Respecter les bonnes pratiques de déploiement et sécurité (Django 5).

---

## Structure du projet

```
reservations/               # Projet principal Django
catalogue/                  # Application interne
requirements.txt            # Liste des dépendances Python
manage.py                   # Commandes Django
README.md                   # Documentation du projet
```

---

## ⚙Installation et configuration

### Installation complète (environnement propre)

Pour une installation depuis zéro :

```bash
git clone https://github.com/mouedarbi/PID_Reservations_Groupe_Django.git
cd PID_Reservations_Groupe_Django
python -m venv .venv
.venv\Scripts\activate      # (Windows)
# ou
source .venv/bin/activate   # (Linux / Mac)
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

L’application est ensuite accessible sur :
👉 [http://localhost:8000](http://localhost:8000)

---

### Chargement des données de test

Après avoir exécuté les migrations (`python manage.py migrate`), vous pouvez peupler la base de données avec un jeu de données de test complet.

Utilisez la commande de gestion personnalisée suivante :

```bash
python manage.py load_all_fixtures
```

Cette commande exécute une série de `loaddata` dans le bon ordre pour garantir l'intégrité des relations entre les modèles.

---

### Réutilisation de l’environnement du Starter Kit

Si vous avez déjà installé le **Starter Kit Django 5** du PID :
vous pouvez simplement **réutiliser le même environnement virtuel**.

1. Placez le dossier `RESERVATION_GROUPE` **au même niveau que** votre dossier `reservations` (Starter Kit) :

   ```
   BACHELIER_ICC/
   ├── StarterKit_Django/
   │   ├── reservations/
   │   └── .virtualenvs/
   ├── RESERVATION_GROUPE/
   │   └── manage.py
   ```

2. Activez le même environnement :

   ```bash
   .virtualenvs\djangodev\Scripts\activate
   ```

3. Vérifiez que Django est bien actif :

   ```bash
   python -m django --version
   ```

4. Depuis le répertoire du projet de groupe :

   ```bash
   cd RESERVATION_GROUPE
   python manage.py migrate
   python manage.py runserver
   ```

Cela évite de recréer un environnement virtuel et garantit que tous les membres du groupe utilisent les **mêmes versions de paquets**.

---

## Technologies utilisées

- Python **3.11+**
- Django **5.0.14**
- MySQL / MariaDB **11+**
- Bootstrap 5
- ReactJS (Itération 7 – Front-end)
- Git / GitHub (collaboration)

---

## Itérations prévues

| N°  | Intitulé                   | Objectif                               |
| --- | -------------------------- | -------------------------------------- |
| 1   | Installation du framework  | Création du projet Django et dépôt Git |
| 2   | Starter Kit                | CRUD simple (Artistes)                 |
| 3   | Mapping relationnel simple | Entités Type, Locality, Price          |
| 4   | Authentification           | Gestion des utilisateurs               |
| 5   | Relations complexes        | Shows, Reservations, Relations         |
| 6   | API RESTful                | Exposition sécurisée des données       |
| 7   | Intégration Frontend       | Interface ReactJS                      |

---

## 📜 Licence

Projet académique – **Bachelier en Informatique de Gestion (PID)**
© 2025 – Tous droits réservés.

<!-- Test comment for CI/CD -->
