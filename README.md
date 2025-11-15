# 🌐 User Flow — Site Web de Gestion de Projets & Suivi clients

Ce document décrit le **parcours utilisateur (User Flow)** du site web, depuis l’arrivée sur la page de connexion jusqu’à la gestion complète des clients, projets et prestations.

---

# 🔐 1. Authentification
## 🔐 1. Page de Connexion

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

## 📊 2. Tableau de Bord — `dashboard`

Contenu :
- Statistiques globales et comparaison de l'évolution en pourcentage par rapport au mois dernier des (projets en cours, projets terminé, tâches en cours)
- Statistique globales des rapport 
- Trois graphes de suivis des ( Tâches journalière terminées, Nombres de projet par mois, Nombres de tâches compltées par mois )
- Une évolution de tout les projets en pourcentage
- Un classe des projets par ordre décroissant de priorité

Navigation possible vers :
- Clients  ( Gestion des clients )
- Projets  ( Gestion des projets ) Nb: Un projets peux avoir un ou plusieurs prestations
- Rapport ( Gestion des rapport )
- Déconnexion  ( Se déconnecter de l'application )

---

# 👥 3. Gestion des Clients

## 📄 3.1. Liste des Clients — `clients`
- Affiche les informations de tout les client
  
Fonctionnalités :
- Ajouter un client
- Modifier un client 
- Supprimer un client  
- Générer un papi pour le client

---

## ➕ 3.2. Ajouter un Client — `clients_add`

Champs :
- Raison sociale
- NIF
- Adresse  
- Email  
- Téléphone  

Action :  
→ Enregistrer → Redirection vers la liste des clients

---

# 📁 4. Gestion des Projets

## 📄 4.1. Liste des Projets — `projets`
- Afficher les informations des projets
  
Fonctionnalités :   
- Ajouter un projet
- Accès aux détails pour voir les prestation ( tâches lier au projet )
- Marquer comme terminé ( les prestation serons automatiquement marquer comme fini )
- Supprimer le projet
- Modifier les information du projet

---

## ➕ 4.2. Ajouter un Projet — `projets_add`

Champs :
- Selectionner le client
- Intitulé
- Description
- Date de début
- Le projet auras une priorité normal a la création
- Cliquer sur **Ajouter les prestations** pour ajouter des prestation sur le projet

---

## 📘 4.3. Détails d’un Projet — `projets`

Contenu :
 - Prestations associées au projet
- Actions :
  - Ajouter une prestation
  - Modifier une prestation
  - Supprimer une prestation
  - Laisser une note
---

# 🛠️ 5. Gestion des Prestations (Tâches)

## 📄 5.1. Liste des Prestations — `prestations`
- Voir toutes les prestations lier a un projet
  
Fonctionnalités :
- Modifier
- Supprimer  
- Ajouter
---

## ➕ 5.2. Ajouter une Prestation — `prestations_add`
- On peut ajouter auttant de prestation a un projet a la création, tout comme on peux le faire après la création du projet
  
Champs :
- Désignation de la prestation
- Département concerner
- Date de fin estimé
- Description
- Cliauer sur **ajouter une autre** pour ajouter une autre prestation
- CLiquer sur **ajouter et quitter** pour ajouter une prestation et être rediriger vers la liste des prestations du projet concerné

---

# ⚙️ 6. Rapport — `Rapport`

- Liste des tous les rapport

Fonctionnalités :
- Ajouter un rapport ( Soumetre un fichier depuis votre gestionnaire de fichier )
- Modifier un rapport ( Ecrassé l'ancien fichier par un autre )
- Télecharger le rapport
- Supprimer le rapport


---

# 🔒 7. Déconnexion — `logout`

- Déconnexion  
- Redirection vers la page de connexion
