# Plan d'implémentation : Système d'Articles de Presse

Ce document détaille les étapes pour implémenter le système d'articles de presse, incluant le workflow de demande pour devenir critique, l'espace de rédaction pour les critiques, et l'espace de modération pour les producteurs.

## 1. Modèles de Données (catalogue/models/)

### CriticRequest
- `user` (FK User)
- `first_name` (CharField)
- `last_name` (CharField)
- `profession` (CharField)
- `media_name` (CharField) : Journal ou média pour lequel il écrit.
- `website` (URLField, optional)
- `motivation` (TextField)
- `status` (pending/approved/rejected)

### PressArticle
- `user` (FK User, critique)
- `show` (FK Show)
- `title` (CharField)
- `summary` (TextField) : Bref résumé pour l'affichage liste.
- `content` (TextField) : Corps de l'article (style blog).
- `validated` (BooleanField) : Validé par le producteur.
- `is_pinned` (BooleanField) : Mis en avant.
- `created_at` (DateTimeField)

## 2. Workflow de Demande Critique (Phase 1)

### Accounts (User Side)
- **Form** : `CriticRequestForm` (nom, prénom, profession, media, site, motivation).
- **View** : `become_critic` - Gère la soumission de la demande.
- **Template** : `become_critic.html` - Formulaire élégant.
- **URL** : `accounts/become-critic/`.

### Admin (Dashboard)
- **View** : `admin_critic_requests` - Liste les demandes en attente.
- **View** : `admin_critic_request_action` - Accepter/Refuser.
- **Template** : `admin/critic_requests.html`.
- **Signal** : Sur approbation, ajouter l'utilisateur au groupe `PRESS_CRITIC`.

## 3. Gestion des Articles de Presse (Phase 2)

### Espace Critique (Profil Utilisateur)
- **Dashboard** : `critic_dashboard` (Mes articles de presse).
- **Form** : `PressArticleForm` (Titre, Résumé, Contenu, Spectacle).
- **View** : `submit_press_article` - Création et édition d'articles.
- **Template** : `user/press_articles.html`.

### Espace Producteur (Modération)
- **Dashboard** : Bouton "Gérer les articles de presse" à côté de "Gérer les avis".
- **View** : `prod_moderate_press_articles` - Liste les articles concernant ses spectacles.
- **View** : `prod_validate_press_article` - Approuver/Refuser/Épingler.
- **Template** : `prod/moderate_press_articles.html`.

## 4. Affichage Frontend (Phase 3)

### Détail Spectacle
- Mise à jour de `show_detail.html` pour inclure une section "Articles de Presse" distincte des avis clients.
- Les articles épinglés apparaissent en premier.

## 5. Validation et Tests
- Création de tests unitaires pour simuler le cycle complet :
  1. Membre -> Demande Critique -> Admin Approuve.
  2. Critique -> Rédige Article -> En attente.
  3. Producteur -> Approuve Article -> Visible en Frontend.
