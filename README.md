# 🌐 User Flow — Site Web de Gestion de Projets & Suivi clients

Ce document décrit le **parcours utilisateur (User Flow)** du site web, depuis l’arrivée sur la page de connexion jusqu’à la gestion complète des clients, projets et prestations.

---

# 🔐 1. Authentification
## 🔐 1. Page de Connexion — `login`

### Actions possibles
- Saisir email / mot de passe  
- Cliquer sur **Connexion**  
- Être redirigé vers le **Dashboard** en cas de succès  
- Cliqier sur **Créer un compte** pour se créer un compte

## 🔐 2. Page d'Inscription

## Actions possibles
- Saisir Nom & Prènom / Nom d'utilisateur / Email / Poste / Département
- Cliquer sur **Créer**
- Être redirigé vers le **Dashboard** en cas de succès
- Cliquer sur **Se connecter** pour se connecter avec un compte existant

---

## 📊 2. Tableau de Bord — `/dashboard/`

Contenu :
- Statistiques globales et comparaison de l'évolution en pourcentage par rapport au mois dernier des (projets en cours, projets terminé, tâches en cours)
- Statistique globales des rapport 
- Graphiques de progression  

Navigation possible vers :
- Clients  
- Projets  
- Prestations  
- Paramètres  
- Déconnexion  

---

# 👥 3. Gestion des Clients

## 📄 3.1. Liste des Clients — `/clients/`

Fonctionnalités :
- Voir tous les clients  
- Ajouter un client  
- Modifier un client  
- Supprimer un client  
- Accéder aux projets liés à un client

---

## ➕ 3.2. Ajouter un Client — `/clients/add/`

Champs :
- Raison sociale  
- Email  
- Téléphone  
- Adresse  

Action :  
→ Enregistrer → Redirection vers la liste des clients

---

## 📘 3.3. Détails d’un Client — `/clients/<id>/`

Contient :
- Informations du client  
- Liste des projets liés  
- Actions :
  - Modifier  
  - Supprimer  
  - Ajouter un projet lié  

---

# 📁 4. Gestion des Projets

## 📄 4.1. Liste des Projets — `/projets/`

Fonctionnalités :
- Affichage des projets  
- Filtre par statut  
- Accès aux détails  
- Ajouter un projet  

---

## ➕ 4.2. Ajouter un Projet — `/projets/add/`

Champs :
- Intitulé  
- Client  
- Description  
- Statut  
- Date de début  
- Date de fin  

---

## 📘 4.3. Détails d’un Projet — `/projets/<id>/`

Contenu :
- Informations complètes  
- Prestations associées  
- Graphiques de progression  
- Actions :
  - Ajouter une prestation  
  - Modifier  
  - Changer le statut  
  - Supprimer  

---

# 🛠️ 5. Gestion des Prestations (Tâches)

## 📄 5.1. Liste des Prestations — `/prestations/`

Fonctionnalités :
- Voir toutes les prestations  
- Filtrer par projet ou statut  
- Modifier  
- Supprimer  

---

## ➕ 5.2. Ajouter une Prestation — `/prestations/add/`

Champs :
- Projet  
- Désignation  
- Direction  
- Description  
- Date de fin  
- Statut  

---

# ⚙️ 6. Paramètres — `/settings/`

- Modifier le profil  
- Changer le mot de passe  
- Préférences générales  

---

# 🔒 7. Déconnexion — `/logout/`

- Déconnexion  
- Redirection vers la page de connexion
