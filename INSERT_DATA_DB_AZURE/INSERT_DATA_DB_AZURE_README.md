# INSERT_DATA_DB_AZURE

Ce dossier contient les scripts pour créer les tables dans la base de donnée Azure. Il contient également des csv à integrer dans la BDD pour avoir un historique dans notre application DJango (avoir accès à des films depuis juillet 2023).

- **utils.py** : script qui contient des fonctions pour se connecter à la BDD et supprimer une table.

- **create_movies_and_actors_table.py** : script pour créer la table "movies" et la table "actors" associé et insérer les données du fichier *dataset_history_django_features.csv*.

- **create_boxoffice_table.py** : script pour créer la table "boxoffice" et insérer les données du fichier *dataset_history_django_boxoffice.csv*.

-- **create_prediction_table.py** : script pour créer la table "prediction" et stocké=er les predictions effectuées par l'API.

- **merging_dataset.ipynb** : ce notebook récupère les fichiers csv issus sur scraping (boxoffice.csv et movies.csv dans le dossier SCRAP_DATA_FOR_THE_MODEL/scrap_allocine/dataset) et les merge. Puis sépare en 2 dataframes :
	- un pour les données avant juillet 2023 (*dataset_model.csv)
	- un pour les données à partir de juillet 2023, qui est séparé en 2 fichiers (cf. ci-dessous)

- **dataset_history_django_features.csv** : contient les films sortie au cinéma depuis le 1er juillet 2023 et leurs informations.

- **dataset_history_django_boxoffice.csv**: contient les boxoffices de la 1ère semaines des films sortis au cinéma depuis le 1er juillet 2023 

Pour executer les fichiers script, executer les commandes suivantes :  
`python create_movies_and_actors_table.py`  
`python create_boxoffice_table.py`  
`python create_prediction_table.py`

La table boxoffice étant lié à la table movies, il faut d'abord créer la table movies pour pouvoir créer la table boxoffice.
