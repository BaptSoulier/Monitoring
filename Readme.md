# Projet de Surveillance du Système de Fichiers

## Description

Ce projet est un outil de surveillance des propriétés des fichiers et de gestion des droits d'accès pour les systèmes d'exploitation Linux. Il permet aux administrateurs système de suivre les modifications apportées aux fichiers et de gérer les autorisations d'accès afin d'assurer la sécurité et l'intégrité des données.

## Fonctionnalités

* Surveillance en temps réel des modifications des propriétés des fichiers (autorisations, propriétaire, date de modification, etc.).
* Enregistrement des événements de modification dans des journaux système.
* Alertes en temps réel pour les modifications suspectes.
* Possibilité d'ajouter et de supprimer des fichiers à surveiller.
* Interface utilisateur pour modifier les autorisations d'accès aux fichiers.
* Gestion des autorisations par utilisateur, groupe d'utilisateurs et autres critères de sécurité.
* Mécanismes de sécurité pour empêcher les accès non autorisés aux fichiers sensibles.
* Vérification de l'intégrité des fichiers pour détecter les modifications non autorisées.
* Interface utilisateur conviviale pour surveiller les événements, afficher les autorisations et les modifier.
* Système d'authentification pour accéder à l'outil.
* Interface en ligne de commande (CLI) pour ajouter et supprimer des fichiers à surveiller.

## Technologies

* Langage de programmation : Python
* Interface utilisateur : Flask (interface web)
* Base de données : MongoDB
* Bibliothèque de surveillance de fichiers : watchdog
* Gestion des permissions : Utilisation des fonctions natives de Python et du module os
* Authentification : Flask-Login
* Formulaires web : Flask-WTF

## Installation

1.  **Cloner le dépôt :**

    ```bash
    git clone <URL_DU_DEPOT>
    cd moniteur_systeme
    ```

2.  **Créer un environnement virtuel :**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Installer les dépendances :**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Installer MongoDB :**

    * Suivez les instructions d'installation pour votre système d'exploitation : [https://www.mongodb.com/docs/manual/installation/](https://www.mongodb.com/docs/manual/installation/)

5.  **Configurer les variables d'environnement :**

    * Définissez les variables d'environnement nécessaires pour que Flask puisse se connecter à MongoDB. Vous pouvez le faire dans votre fichier de configuration de shell (par exemple, `~/.bashrc` ou `~/.zshrc`) ou temporairement dans votre terminal :

        ```bash
        export SECRET_KEY="une_cle_secrete_tres_difficile"  # Changez ceci
        export MONGO_URI="mongodb://localhost:27017/moniteur_systeme"  # URI de connexion MongoDB
        export MONGO_DBNAME="moniteur_systeme" # Nom de la base de données
        ```

6.  **Lancer l'application :**

    ```bash
    python run.py
    ```

7.  **Accéder à l'interface utilisateur :**

    * Ouvrez un navigateur web et accédez à l'adresse indiquée par Flask (généralement `http://127.0.0.1:5000`).

## Configuration

* **`config/app_config.py`**: Contient les paramètres de configuration de l'application, y compris les paramètres de la base de données, la clé secrète et les chemins des fichiers de log.
* **`webapp/\_\_init\_\_.py`**: Initialise l'application Flask, configure la journalisation, la base de données et enregistre les blueprints.
* **`database/db.py`**: Gère la connexion à la base de données MongoDB.
* **`core/log_manager.py`**: Gère l'enregistrement des événements dans la base de données et les fichiers de log.
* **`core/file_watcher.py`**: Surveille les modifications apportées aux fichiers à l'aide de la bibliothèque `watchdog`.
* **`core/permission_manager.py`**: Gère la récupération et la modification des permissions des fichiers.
* **`core/utils.py`**: Contient des fonctions utilitaires pour valider les chemins de fichiers et calculer les sommes de contrôle.
* **`webapp/routes.py`**: Définit les routes de l'application web Flask.
* **`webapp/forms.py`**: Définit les formulaires utilisés dans l'application web.
* **`webapp/templates/`**: Contient les fichiers HTML pour l'interface web.

Structure du projet

moniteur_systeme/
├── config/
│   ├── app_config.py
│   └── __init__.py
├── core/
│   ├── file_watcher.py
│   ├── log_manager.py
│   ├── permission_manager.py
│   ├── utils.py
│   └── __init__.py
├── database/
│   ├── db.py
│   └── __init__.py
├── logs/
├── webapp/
│   ├── forms.py
│   ├── routes.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   └── permissions.html
│   ├── __init__.py
├── requirements.txt
├── run.py
└── README.md