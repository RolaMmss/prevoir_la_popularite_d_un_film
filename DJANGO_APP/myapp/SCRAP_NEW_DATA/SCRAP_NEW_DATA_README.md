# SCRAP_NEW_DATA

Ce dossier contient un projet scrapy **scrap_films_prochainement** avec 2 spiders :  

- **next_movies.py** : spider pour scraper les fims à venir, disponilbes à cette adresse : https://www.allocine.fr/film/agenda

- **boxoffice_spider.py** : spider pour scraper le boxoffice de la 1ère semaine dès films sorti récemment, à cette adresse : https://www.allocine.fr/boxoffice/france/

Le fichier **pipeline.py** défini différentes pipelines : 
- des pipelines de prétraitement des données scrapées, pour obtenir le format désiré.
- une pipeline qui exporte les données dans des fichiers csv (dans le dossier dataset)
- une pipeline qui exporte les données directement dans la BDD Azure dans les tables "movies", "acteurs" et "boxoffice".

Ces spiders sont exectués depuis l'application django, par un clique de l'utilisateur sur les boutons approprié depuis la page "Boxoffice Forecast" et défini dans les vues *scraping_boxoffice_view* et *scraping_view*.

