# 🧾 Journal de Bord – Implémentation du Starter Kit Django 5
**Projet :** Réservations (PID)  
**Étudiant :** Mohamed Ouedarbi  
**Framework :** Django 5 + MySQL  
**Période :** Octobre 2025  

---

## 📅 04/10/2025 – Initialisation du projet

**Contexte :**
- Création du dépôt GitHub de groupe.  
- Clonage local et configuration initiale du projet Django.  
- Ajout du fichier `.gitignore` et suppression du dossier `.virtualenvs` du dépôt.  
- Premier commit : *initial Django project setup*.

**Résultat :**  
Projet Django 5 initialisé avec structure standard (`reservations/`, `catalogue/`, `manage.py`).

---

## 📅 05/10/2025 – Configuration de l’environnement Django

**Actions réalisées :**
- Ajout du fichier `.env` (variables MySQL).  
- Installation de `mysqlclient` et création de la base de données `reservations`.  
- Exécution de `makemigrations` et `migrate`.  
- Création du superutilisateur Django.  

**Problème rencontré :**
```
fatal: The current branch dev_mohamed has no upstream branch.
```

**Cause :**
La branche locale `dev_mohamed` n’était pas reliée à la branche distante.

**Résolution :**
```bash
git branch --set-upstream-to=origin/dev_mohamed dev_mohamed
```

**Résultat :**  
Branche synchronisée avec GitHub, push/pull fonctionnent correctement.

---

## 📅 06/10/2025 – Lancement du serveur Django et gestion des routes

**Problème :**
```
Page not found (404)
The empty path didn’t match any of these.
```

**Cause :**
Aucune route définie pour la racine `/` dans `reservations/urls.py`.

**Résolution (Starter Kit officiel) :**
```python
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('catalogue/', include('catalogue.urls')),
    path('admin/', admin.site.urls),
]
```

**Résultat :**  
Ajout d’une page d’accueil (ou redirection vers `/catalogue/`).

---

## 📅 06/10/2025 – App `catalogue` inaccessible

**Erreur :**
```
Page not found (404) – /catalogue/
```

**Cause :**
`catalogue/urls.py` appelait des fonctions inexistantes :
```python
views.artist.index
```
alors que `views/__init__.py` importait déjà les vues directement.

**Résolution :**
```python
urlpatterns = [
    path('artist/', views.index, name='artist-index'),
    path('artist/<int:artist_id>/', views.show, name='artist-show'),
]
```

**Résultat :**  
Les routes `/catalogue/artist/` et `/catalogue/artist/<id>/` fonctionnent.

---

## 📅 06/10/2025 – Erreur persistante sur `/`

**Message :**
```
The empty path didn’t match any of these.
```

**Cause :**
Toujours aucune route définie pour la racine `/`.

**Résolution rapide (redirection automatique) :**
```python
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/artist/', permanent=False)),
    path('artist/', include('catalogue.urls')),
    path('admin/', admin.site.urls),
]
```

**Résultat :**  
La racine `/` redirige désormais vers `/artist/`.

---
## 📅 20/10/2025 – Correction du module Artist (Formulaire Edit)

**Contexte :**  
Travail sur la vue `edit` du modèle `Artist` et test du formulaire de modification dans PyCharm.  

---

### 🧩 Erreur 1 – Route inexistante

**Message :**  
`NoReverseMatch: Reverse for 'artist-update' not found.`  

**Cause :**  
Le formulaire HTML appelait une route `artist-update` absente de `urls.py`.  

**Résolution :**  
Remplacement de la référence par la route existante `artist-edit`.  

**Statut :** ✅ Résolu  

---

### 🧩 Erreur 2 – CSRF verification failed

**Message :**  
`CSRF verification failed. Request aborted.`  

**Cause :**  
La balise Django était mal orthographiée (`cfr_token` au lieu de `csrf_token`).  

**Résolution :**  
Correction du nom de la balise dans le formulaire HTML.  

**Statut :** ✅ Résolu  

---

### 🧩 Erreur 3 – PyCharm ne reconnaissait pas Django

**Message :**  
`Unresolved reference 'django'`  

**Cause :**  
L’environnement virtuel `.virtualenvs\\djangodev` n’était pas sélectionné dans les paramètres du projet PyCharm.  

**Résolution :**  
Ajout manuel de l’interpréteur Python depuis le chemin :  
`C:\\Users\\moued\\.virtualenvs\\djangodev\\Scripts\\python.exe`  

**Statut :** ✅ Résolu  

---

## 📅 20/10/2025 – Vérifications finales

| URL | Résultat attendu | Statut |
|------|------------------|--------|
| `/admin/` | Interface d’administration Django | ✅ |
| `/artist/` | Liste des artistes (vue `index`) | ✅ |
| `/artist/<id>` | Détail d’un artiste (vue `show`) | ✅ |
| `/` | Redirection vers `/artist/` | ✅ |

---

## 🧩 Résumé général

| Étape | Type d’erreur | Origine | Statut |
|-------|----------------|----------|---------|
| Configuration Git | “No upstream branch” | Synchronisation GitHub | ✅ Résolu |
| Page d’accueil 404 | Route vide manquante | `reservations/urls.py` | ✅ Résolu |
| /catalogue/ non trouvé | Mauvaise référence de vue | `catalogue/urls.py` | ✅ Résolu |
| / toujours 404 | Absence de redirection | `RedirectView` ajouté | ✅ Résolu |

---

## ✅ État final du projet (20/10/2025)
- Serveur Django fonctionnel ✔️  
- Connexion MySQL opérationnelle ✔️  
- Routes `/`, `/artist/`, `/admin/` accessibles ✔️  
- Branches Git synchronisées ✔️  
- Starter Kit complètement implémenté ✔️  

---

**Auteur :**  
Mohamed Ouedarbi – Bachelier en Informatique de gestion  
📅 Dernière mise à jour : 20/10/2025



**Auteur :**  
Mohamed Ouedarbi – Bachelier en Informatique de gestion  
📅 Dernière mise à jour : 06/10/2025

