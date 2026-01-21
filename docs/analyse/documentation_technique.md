# Documentation technique minimale  
**Projet PID – Réservations**

---

## 1. Architecture générale

L’application est une **application Web dynamique** basée sur une architecture **MVC** fournie par le framework **Django**.

### Couches principales
- **Frontend**
  - Templates HTML (Django Templates)
  - CSS (Bootstrap ou Tailwind)
  - JavaScript (vanilla / jQuery, AJAX)
- **Backend**
  - Framework : Django
  - Logique métier dans les views et services
  - ORM Django pour l’accès aux données
- **Base de données**
  - Base relationnelle (SQLite en développement, PostgreSQL possible)
- **Services externes**
  - Web service tiers (catalogue spectacles)
  - Service de paiement
- **API interne**
  - API REST sécurisée pour affiliés
  - Flux RSS généré par l’application

---

## 2. Organisation du projet Django

Structure logique prévue :

- `accounts`
  - Gestion des utilisateurs
  - Authentification / rôles
- `catalogue`
  - Spectacles, artistes, lieux, représentations
- `reservations`
  - Réservations et billets
- `reviews`
  - Commentaires et critiques
- `api`
  - Exposition des données REST
- `admin_backoffice`
  - Interface d’administration sécurisée

---

## 3. Modèles de données principaux

### Utilisateurs
- `User`
  - username
  - password (hashé)
  - firstname
  - lastname
  - email
  - language
- `Role`
  - public
  - member
  - admin
  - affiliate
  - producer
  - press_critic

---

### Artistes
- `Artist`
  - id
  - firstname
  - lastname
- `Type`
  - id
  - type (fonction : comédien, auteur, etc.)
- `ArtistType`
  - artist_id
  - type_id

---

### Spectacles
- `Show`
  - id
  - title
  - slug
  - description
  - poster_url
  - bookable
  - price
  - location_id
  - created_at

---

### Lieux
- `Locality`
  - id
  - postal_code
  - locality
- `Location`
  - id
  - designation
  - address
  - website
  - phone
  - locality_id

---

### Représentations
- `Representation`
  - id
  - show_id
  - date
  - time
  - location_id
  - is_full

---

### Réservations
- `Reservation`
  - id
  - user_id
  - representation_id
  - created_at
- `ReservationItem`
  - reservation_id
  - quantity
  - price_id

---

### Commentaires et critiques
- `Review`
  - id
  - user_id
  - show_id
  - content
  - rating
  - validated
- `PressReview`
  - id
  - user_id
  - show_id
  - link_or_text
  - status

---

## 4. API REST (interne)

### Authentification
- Token ou JWT
- Accès basé sur le rôle (Free / Starter / Premium)

### Endpoints principaux
- `GET /api/shows`
- `GET /api/shows/{id}`
- `GET /api/representations`
- `GET /api/locations`
- `GET /api/artists`

### Restrictions
- Limitation du nombre de requêtes
- Filtrage des champs selon le niveau d’abonnement

---

## 5. Flux RSS

- Flux des prochaines représentations
- Généré automatiquement depuis les données `Representation`
- Accessible publiquement

---

## 6. Sécurité

- Authentification Django (sessions, tokens)
- Hashage des mots de passe
- Protection CSRF
- Validation serveur systématique
- Protection contre :
  - Injections SQL (ORM)
  - XSS
  - Vol de session
- Gestion des permissions par rôle

---

## 7. Import / Export de données

- Import XML initial vers la base de données
- Import / export CSV depuis le back-office
- Export possible pour statistiques et reporting

---

## 8. Back-office Administrateur

Fonctionnalités :
- CRUD complet sur :
  - Spectacles
  - Artistes
  - Lieux
  - Représentations
- Modération des commentaires
- Gestion des utilisateurs et rôles
- Configuration générale de l’application

---

## 9. Contraintes techniques respectées

- Programmation orientée objet
- Framework backend : Django
- ORM pour la persistance
- Architecture MVC
- Sécurité intégrée
- Préparation à une API RESTful
- Compatibilité future avec frontend Vue.js

---

## 10. Limites de la version Alpha

- Fonctionnalités non exhaustives
- Frontend simplifié (templates Django)
- API partiellement implémentée
- Objectif : MVP fonctionnel sans bug bloquant

---
