# 🎝️ Projet PID – Réservations (Django 5 + MySQL)

## 1️⃣ Objectif du projet

Ce projet s’inscrit dans le cadre du **PID – Projet Réservations**, réalisé dans le cursus du Bachelier en Informatique de gestion.

L’objectif est d’**informatisé la gestion des réservations de spectacles** pour une société de production, au moyen du framework **Django 5 (Python)** et d’une base de données **MySQL ou MariaDB**.

Chaque membre du groupe installe et configure **son propre environnement local**, de manière à ce que le projet soit portable, reproductible et hébergeable sur un serveur distant à la fin du développement.

---

## 2️⃣ Pré-requis système

Avant d’installer le projet, vérifie que ta machine dispose de :

| Logiciel                            | Version minimale | Vérification            |
| ----------------------------------- | ---------------- | ----------------------- |
| **Python**                          | 3.11 ou 3.12     | `python --version`      |
| **pip**                             | ≥ 24             | `pip --version`         |
| **Git**                             | ≥ 2.40           | `git --version`         |
| **MySQL / MariaDB**                 | ≥ 8.0 ou ≥ 10.5  | `mysql --version`       |
| **Virtualenv** (inclus avec Python) | –                | `python -m venv --help` |

Chaque membre doit avoir son environnement Python et sa base MySQL ou MariaDB **fonctionnels et accessibles via le terminal**.

---

## 3️⃣ Installation du projet (étapes de mise en place)

### Étape 1 – Créer un environnement virtuel

* Créer un dossier du projet (par ex. `RESERVATION`)
* Exécuter : `python -m venv .virtualenvs\djangodev`
* Activer l’environnement virtuel :
  `\.virtualenvs\djangodev\Scripts\activate`

### Étape 2 – Installer Django

* Installer la version stable de Django 5 :
  `pip install "Django==5.0.*"`
* Vérifier : `django-admin --version`

### Étape 3 – Créer le projet et l’application

* Créer le projet principal :
  `django-admin startproject reservations .`
* Créer l’application interne :
  `python manage.py startapp catalogue`
* Ajouter `'catalogue',` dans `settings.py` sous `INSTALLED_APPS`.

### Étape 4 – Installer et configurer MySQL

* Installer **MySQL 8.4 LTS** (ou MariaDB 11.x)
* Vérifier : `mysql --version`
* Créer une base de données :

  ```sql
  CREATE DATABASE reservations CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
  ```
* Créer un utilisateur (optionnel) :

  ```sql
  CREATE USER 'django_user'@'localhost' IDENTIFIED BY 'Django123!';
  GRANT ALL PRIVILEGES ON reservations.* TO 'django_user'@'localhost';
  FLUSH PRIVILEGES;
  ```

### Étape 5 – Connecter Django à MySQL

Dans `reservations/settings.py`, modifier la section `DATABASES` :

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'reservations',
        'USER': 'root',  # ou django_user
        'PASSWORD': 'ton_mot_de_passe',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

### Étape 6 – Effectuer les migrations

Exécuter :

```bash
python manage.py migrate
```

Si tout fonctionne, Django crée automatiquement ses tables système dans la base de données.

### Étape 7 – Créer un compte administrateur

Exécuter :

```bash
python manage.py createsuperuser
```

Ce compte te permettra d’accéder à l’interface d’administration sur
👉 [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

---

## 4️⃣ Vérifications à effectuer

Chaque membre du groupe doit s’assurer que :

| Vérification          | Commande                                                   | Résultat attendu                  |
| --------------------- | ---------------------------------------------------------- | --------------------------------- |
| Version Python        | `python --version`                                         | Python 3.11.x ou 3.12.x           |
| Django installé       | `django-admin --version`                                   | 5.0.x                             |
| Serveur MySQL actif   | `mysql --version`                                          | 8.x (ou 11.x pour MariaDB)        |
| Environnement activé  | `(djangodev)` visible dans le terminal                     | Oui                               |
| Migrations effectuées | `python manage.py migrate`                                 | Toutes en “OK”                    |
| Serveur Django        | `python manage.py runserver`                               | Page “Congratulations” accessible |
| Interface admin       | [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) | Login admin fonctionnel           |

---

## 5️⃣ Structure du projet attendue

```
RESERVATION/
│
├── .virtualenvs/
│   └── djangodev/
│
├── catalogue/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   └── ...
│
├── reservations/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── manage.py
└── README.md
```

---

## 6️⃣ Fichier `.env` (configuration locale)

Chaque membre du groupe doit créer **un fichier `.env` à la racine du projet** contenant ses propres informations de base de données (non partagées sur GitHub).

Exemple :

```env
DB_NAME=reservations
DB_USER=root
DB_PASSWORD=ton_mot_de_passe
DB_HOST=127.0.0.1
DB_PORT=3306
```

Le fichier `.env` ne doit **pas** être ajouté à Git.
Ajoutez-le au fichier `.gitignore` :

```
.env
```

Django chargera automatiquement ces variables via `python-dotenv` (installé ultérieurement).

---

## 7️⃣ Test final de fonctionnement

Pour vérifier que tout est bien en place :

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Puis ouvre [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
Tu dois voir la page Django par défaut.
Connecte-toi ensuite à [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) avec ton compte superutilisateur.

---

## ✅ Résultat attendu

À ce stade, chaque membre du groupe doit avoir :

* un environnement Django 5 fonctionnel,
* une base MySQL/MariaDB connectée,
* les migrations appliquées,
* un compte administrateur actif,
* et le projet prêt pour l’étape suivante du Starter Kit :
  **le mapping de la première entité (`Type`) et les opérations CRUD.**
