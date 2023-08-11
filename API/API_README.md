# Documentation de l'API de Prédiction de Box Office de Films


## Description

Ce projet consiste en une API basée sur FastAPI qui permet de prédire le box office d'un film en fonction de ses caractéristiques. L'API utilise un modèle pré-entraîné pour effectuer ces prédictions.

## Installation

1. Cloner ce dépôt sur votre machine locale.
2. Assurez-vous que vous avez toutes les dépendances requises installées. Vous pouvez les installer en exécutant `pip install -r requirements.txt` dans le répertoire du projet.
3. Assurez-vous d'avoir placé le fichier du modèle pré-entraîné (`best_model.joblib`) dans le même répertoire que les fichiers de l'API.
4. creer un fichier .env dans le dossier API en notant les infos de connexion a la bdd azure suivants :
DB_USER='sqladmincinema'
DB_PASSWORD='Simplon@123456789'
DB_SERVER='rg-ousfia.database.windows.net'
DB_name='BDD_Cinéma_ IA'
DB_Driver='ODBC Driver 18 for SQL Server'
5.executer ces commandes une part une pour linstallation des dependences des fichiers driver_odbc et install_dependies: -sudo apt-get update,
sudo apt-get install unixodbc-dev, chmod +x Driver_ODBC_Azure.sh
,./Driver_ODBC_Azure.sh,chmod +x install_dependencies.sh,./install_dependencies.sh





## Utilisation

1. Exécutez l'API en exécutant le fichier `main.py` à l'aide de la commande `uvicorn main:app --reload`.
2. Accédez à l'URL [http://localhost:8000/docs](http://localhost:8000/docs) dans votre navigateur pour accéder à l'interface Swagger de l'API. Vous pouvez utiliser cette interface pour tester les points d'extrémité de l'API.
3. Modifier l'url de fastapi et ajouter /docs pour entrer sur la page des endpoints.
4. Utilisez le point d'extrémité `/predict/` pour prédire le box office d'un film en fournissant le titre du film en tant que paramètre.

## Fonctionnement

Le code se compose de deux principaux fichiers : `crud.py` et `main.py`.

### `crud.py`

Ce fichier contient une fonction `update_from_azure_db()` qui effectue les opérations suivantes :

1. Établir une connexion à une base de données Azure SQL à l'aide de la bibliothèque `pyodbc`.
2. Exécuter une requête SQL pour récupérer les données des films, notamment le titre, la durée, le distributeur, le réalisateur, les nationalités, la langue d'origine, le type de film, les genres, l'année de production, les acteurs et les acteurs connus.
3. Nettoyer et transformer les données en remplaçant les valeurs manquantes par des valeurs spécifiques (0 pour 'durée' et 'annee_production', 'inconnu' pour les autres colonnes).
4. Effectuer des opérations de nettoyage supplémentaires, telles que le nettoyage des noms d'acteurs, le calcul du nombre d'acteurs connus et la création de colonnes pour chaque genre de film.
5. Renvoyer un DataFrame avec les données nettoyées et préparées.