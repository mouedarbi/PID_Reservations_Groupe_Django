# 🎝️ Projet PID – Réservations (Django 5 + MySQL)

## 1️⃣ Objectif du projet

Ce projet s’inscrit dans le cadre du **PID – Projet Réservations**, réalisé en groupe dans le cursus du **Bachelier en Informatique de gestion**.

L’objectif est de développer une application web Django pour la **gestion des réservations de spectacles**, avec une base de données **MySQL/MariaDB**, un **back-office sécurisé** et un **catalogue public**.

Chaque membre du groupe travaille sur une **branche Git personnelle**, puis fusionne son travail dans la branche principale (`main`) après validation.

---

## 2️⃣ Pré-requis avant de cloner le projet

Chaque membre doit **préparer sa machine** avant de cloner le dépôt GitHub.

| Logiciel            | Version minimale   | Vérification            |
| ------------------- | ------------------ | ----------------------- |
| **Python**          | 3.11 ou 3.12       | `python --version`      |
| **pip**             | ≥ 24               | `pip --version`         |
| **Git**             | ≥ 2.40             | `git --version`         |
| **MySQL / MariaDB** | ≥ 8.0 / ≥ 10.5     | `mysql --version`       |
| **Virtualenv**      | inclus avec Python | `python -m venv --help` |

---

## 3️⃣ Installation de MySQL / MariaDB

### 🧹 Étape 1 – Télécharger MySQL

1. Rendez-vous sur le site officiel :
   👉 [https://dev.mysql.com/downloads/installer/](https://dev.mysql.com/downloads/installer/)
2. Téléchargez le fichier **MySQL Installer (Windows)**.
3. Choisissez le type d’installation :

   * **Developer Default** → installe MySQL Server, MySQL Workbench, et les utilitaires nécessaires.
4. Suivez l’assistant jusqu’à la fin, puis **notez le mot de passe root** que vous définissez.

### 🧹 Étape 2 – Vérifier l’installation

Ouvre un terminal (CMD) et exécute :

```bash
mysql --version
```

Puis connecte-toi au serveur pour tester :

```bash
mysql -u root -p
```

Si la console MySQL s’ouvre sans erreur, tout est prêt ✅.

---

## 4️⃣ Installation du projet Django

### Étape 1 – Cloner le dépôt GitHub

```bash
git clone https://github.com/[nom_du_compte]/ProjetReservations_Django5.git
cd ProjetReservations_Django5
```

### Étape 2 – Créer et activer un environnement virtuel

```bash
python -m venv .virtualenvs\\djangodev
.virtualenvs\\djangodev\\Scripts\\activate
```

Tu sauras que tout est bon si tu vois `(djangodev)` au début de la ligne de commande.

### Étape 3 – Installer les dépendances Python

```bash
pip install -r requirements.txt
```

Si le fichier `requirements.txt` n’est pas encore présent, installe manuellement :

```bash
pip install "Django==5.0.*"
pip install mysqlclient
pip install python-dotenv
```

---

## 5️⃣ Configuration locale (.env + base MySQL)

### Étape 1 – Créer la base MySQL

Connecte-toi à MySQL via le terminal :

```bash
mysql -u root -p
```

Puis exécute :

```sql
CREATE DATABASE reservations CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

-- (Optionnel) Crée un utilisateur dédié :
CREATE USER 'django_user'@'localhost' IDENTIFIED BY 'Django123!';
GRANT ALL PRIVILEGES ON reservations.* TO 'django_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Étape 2 – Créer le fichier `.env` à la racine du projet

```
DB_NAME=reservations
DB_USER=root
DB_PASSWORD=ton_mot_de_passe
DB_HOST=127.0.0.1
DB_PORT=3306
```

⚠️ **Ne jamais versionner ce fichier !**
Ajoute-le à ton `.gitignore` :

```
.env
```

---

## 6️⃣ Configurer Django pour la base de données

Dans `reservations/settings.py`, vérifie que la section `DATABASES` est conforme :

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'reservations',
        'USER': 'root',  # ou 'django_user'
        'PASSWORD': 'ton_mot_de_passe',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

---

## 7️⃣ Lancer le projet localement

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

➡️ Visite [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
➡️ Accède à [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) pour te connecter avec ton superutilisateur.

---

## 8️⃣ Workflow Git (travail collaboratif)

### 🧩 Étape 1 – Créer ta branche de travail

```bash
git checkout -b prenom-dev
```

### 🧩 Étape 2 – Travailler et enregistrer les modifications

```bash
git add .
git commit -m "Ajout du modèle Artist"
git push origin prenom-dev
```

### 🧩 Étape 3 – Fusionner dans `main`

Sur GitHub → **Pull Requests** → **New Pull Request**
Demande une relecture à un autre membre avant de fusionner.

---

## 9️⃣ Vérifications finales

| Vérification    | Commande                                                   | Résultat attendu       |
| --------------- | ---------------------------------------------------------- | ---------------------- |
| Python actif    | `python --version`                                         | 3.11.x ou 3.12.x       |
| Django installé | `django-admin --version`                                   | 5.0.x                  |
| MySQL actif     | `mysql --version`                                          | ≥ 8.0                  |
| Migrations OK   | `python manage.py migrate`                                 | ✔ Toutes réussies      |
| Serveur web     | `python manage.py runserver`                               | Page “Congratulations” |
| Interface admin | [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) | Login admin valide     |

---

## 🔄 Résumé rapide pour un collaborateur

1. Installer **Python**, **Git**, et **MySQL** avec l’exécutable.
2. Vérifier les versions avec `--version`.
3. Cloner le dépôt GitHub.
4. Créer l’environnement virtuel et activer.
5. Installer les dépendances (`pip install -r requirements.txt`).
6. Créer la base `reservations` dans MySQL.
7. Créer le fichier `.env`.
8. Lancer `python manage.py migrate` + `runserver`.
9. Créer ta branche et commencer ton travail.
10. Faire des commits et ouvrir une Pull Request.

