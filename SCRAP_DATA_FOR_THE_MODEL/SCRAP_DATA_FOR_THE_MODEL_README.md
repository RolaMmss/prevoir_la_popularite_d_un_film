# SCRAP_DATA_FOR_THE_MODEL

Ce dossier contient un projet scrapy **scrap_allocine** avec 3 spiders :  

- **films_spider.py** : spider pour scraper l'ensemble des films disponibles sur allociné à cette adresse : https://www.allocine.fr/films/

- **boxoffice_spider.py** : spider pour scraper le boxoffice de la 1ère semaine de tous les films sur allociné 

- **top_acteurs_spider.py** : spider pour scraper la liste des tops acteurs/réalisateurs sur allociné, dsiponible à cette adresse https://www.allocine.fr/personne/top/les-plus-vues/ever/

Pour executer les spiders, executer les commandes suivantes depuis le dossier spider: 
`scrapy crawl nom_du_spider`   (sans l'extension .py)

Le fichier **pipeline.py** défini différentes pipelines : 
- des pipelines de prétraitement des données scrapées, pour obtenir le format désiré.
- une pipeline qui exporte les données dans des fichiers csv (dans le dossier dataset)


