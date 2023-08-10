# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter
import os
from .utils import convert_to_dd_mm_aaaa, convert_to_minutes
import re 
import os
import pypyodbc as odbc
import pyodbc

class CsvPipeline(object):
    def __init__(self, csv_file, fields_to_export):
        self.csv_file = csv_file
        self.fields_to_export = fields_to_export
        self.file = None
        self.exporter = None

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        csv_file = settings.get('CSV_OUTPUT_FILE', 'items.csv')
        fields_to_export = settings.get('CSV_FIELDS_TO_EXPORT', [])
        return cls(csv_file, fields_to_export)

    def open_spider(self, spider):
        # Obtenir le chemin absolu du dossier parent
        parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Concaténer le chemin absolu du dossier parent avec le nom du dossier "dataset" et le nom du fichier CSV
        csv_file_path = os.path.join(parent_directory, 'dataset', self.csv_file)

        # Ouvrir le fichier pour écriture binaire
        self.file = open(csv_file_path, 'wb')

        # Initialiser l'exportateur CSV
        self.exporter = CsvItemExporter(self.file, fields_to_export=self.fields_to_export)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class ProcessPipeline:
    def process_item(self, item, spider):
    
        adapter = ItemAdapter(item)
        
        field_names = ['titre', 'date', 'genre', 'duree', 'realisateur', 'distributeur', 
                             'nationalites', 'langue_d_origine', 'type_film', 'annee_production','nombre_article', 
                              'description']
                  
        ## Strip all whitspaces from strings and handle lists
        for field_name in field_names:
            value = adapter.get(field_name)
            if field_name is not isinstance(value, list):
                # Convert the value to a string if it's not already
                adapter[field_name] = str(value).strip()
        
        ## Process the duree field
        duree_value = adapter.get('duree')
        adapter['duree'] = convert_to_minutes(duree_value)
        
        ## Process the genre field
        genre_value = adapter.get('genre')
        if genre_value is not None and isinstance(genre_value, str):
            # Split the genres by comma and strip whitespace
            genres = [genre.strip() for genre in genre_value.split(',')]
            # Filter out genres containing '/' or digits
            genres = [genre for genre in genres if not re.search(r'[/\d]', genre)]
            # Join the genres back into a single string separated by underscores
            genres_str = "_".join(sorted(genres))
            # Remove quotes and brackets
            genres_str = re.sub(r"['\"\[\]]", "", genres_str)
            adapter['genre'] = genres_str

        ## Process the nombre_article field
        nombre_article_value = adapter.get('nombre_article')
        if nombre_article_value is not None and isinstance(nombre_article_value, str):
            # Use regular expression to extract the number from the text
            number_match = re.search(r'\d+', nombre_article_value)
            if number_match:
                # Convert the extracted number to an integer
                extracted_number = int(number_match.group())
                adapter['nombre_article'] = extracted_number 
            
        return item


class BoxOfficePipeline:
    def process_item(self, item, spider):
        if 'fin_semaine_1' in item:
            fin_semaine_1 = item['fin_semaine_1']
            if 'au' in fin_semaine_1:
                _, date = fin_semaine_1.split('au')
                item['fin_semaine_1'] = convert_to_dd_mm_aaaa(date.strip())
        # Vérifier si les champs 'boxoffice_1' et 'boxoffice_2' existent dans l'item et les convertir en int
        if 'boxoffice_1' in item:
            boxoffice_1 = item['boxoffice_1']
            if boxoffice_1 is not None:
                item['boxoffice_1'] = int(boxoffice_1.replace(' ', ''))

        if 'boxoffice_2' in item:
            boxoffice_2 = item['boxoffice_2']
            if boxoffice_2 is not None:
                item['boxoffice_2'] = int(boxoffice_2.replace(' ', ''))

        return item


# import os
# import pyodbc
# from dotenv import load_dotenv
# from scrapy.exceptions import DropItem

# class AzureSQLPipeline:
#     def __init__(self):
#         load_dotenv()
#         self.username = os.getenv('DB_USER')
#         self.password = os.getenv('DB_PASSWORD')
#         self.server = os.getenv('DB_SERVER')
#         self.database = os.getenv('DB_name')
#         self.DB_Driver = os.getenv('DB_Driver')
#         self.spider_name = None

#     def open_spider(self, spider):
#         self.spider_name = spider.name
        
#         if spider.name == 'top_acteurs_spider':
#             # Établir la connexion
#             connection_string = f'Driver={self.DB_Driver};Server=tcp:{self.server},1433;Database={self.database};Uid={self.username};Pwd={self.password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
#             self.conn = pyodbc.connect(connection_string)
#             self.cursor = self.conn.cursor()

#             self.delete_table('top_acteurs')

#             # Créer la table "top_acteur"
#             create_top_acteur_table_query = '''
#             CREATE TABLE top_acteur (
#                 id INT IDENTITY(1,1) PRIMARY KEY,
#                 acteur VARCHAR(500)
#             );
#             '''
#             self.cursor.execute(create_top_acteur_table_query)
#             self.conn.commit()

        
#         if self.spider_name == 'films_spider':
#             # Établir la connexion
#             connection_string = f'Driver={self.DB_Driver};Server=tcp:{self.server},1433;Database={self.database};Uid={self.username};Pwd={self.password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
#             self.conn = pyodbc.connect(connection_string)
#             self.cursor = self.conn.cursor()

#             # Delete les tables s'il existent
#             self.delete_table('boxoffice')
#             self.delete_table('acteurs_films')
#             self.delete_table('films')


#             # Créer la table "films"
#             create_table_query = '''
#             CREATE TABLE films (
#                 id INT IDENTITY(1,1) PRIMARY KEY,
#                 titre VARCHAR(500),
#                 date VARCHAR(500),
#                 duree VARCHAR(500),
#                 realisateur VARCHAR(500),
#                 distributeur VARCHAR(500),
#                 nationalites VARCHAR(500),
#                 langue_d_origine VARCHAR(500),
#                 type_film VARCHAR(500),
#                 annee_production VARCHAR(500),
#                 nombre_article VARCHAR(500),
#                 description VARCHAR(2000),
#                 genre VARCHAR (1000),
#                 film_id_allocine VARCHAR(10),
#                 image VARCHAR(1000)
#             );
#             '''
#             self.cursor.execute(create_table_query)
#             self.conn.commit()
            
            
#             # Créer la table "acteurs_films"
#             create_acteurs_films_table_query = '''
#             CREATE TABLE acteurs_films (
#                 id_acteurs_films INT IDENTITY(1,1) PRIMARY KEY,
#                 film_id INT,
#                 acteurs VARCHAR(500),
#                 FOREIGN KEY (film_id) REFERENCES films(id)
#                     );
#                 '''
#             self.cursor.execute(create_acteurs_films_table_query)
#             self.conn.commit()

#         if spider.name == 'boxoffice_spider':
#             # Établir la connexion
#             connection_string = f'Driver={self.DB_Driver};Server=tcp:{self.server},1433;Database={self.database};Uid={self.username};Pwd={self.password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
#             self.conn = pyodbc.connect(connection_string)
#             self.cursor = self.conn.cursor()

#             self.delete_table('boxoffice')

#             # Créer la table "top_acteur"
#             create_boxoffice_table_query = '''
#             CREATE TABLE boxoffice (
#                 id INT IDENTITY(1,1) PRIMARY KEY,
#                 titre VARCHAR(500),
#                 fin_semaine_1 VARCHAR(500),
#                 boxoffice_1 INT, 
#                 boxoffice_2 INT,
#                 film_id_allocine INT,
#                 film_id INT,
#                 FOREIGN KEY (film_id) REFERENCES films(id)
#                     );
#             '''
#             self.cursor.execute(create_boxoffice_table_query)
#             self.conn.commit()

#     def delete_table(self, table_name):
#         drop_table_query = f'DROP TABLE IF EXISTS {table_name};'
#         self.cursor.execute(drop_table_query)
#         self.conn.commit()

#     def close_spider(self, spider):
#         if self.spider_name == 'films_spider':
#             self.conn.close()

#     def process_item(self, item, spider):
#         if self.spider_name == 'films_spider':
#             try:
#                 query = '''
#                 INSERT INTO films (titre, date, duree, genre, realisateur, distributeur, nationalites, langue_d_origine, type_film, annee_production, nombre_article, description, film_id_allocine, image)
#                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
#                 '''
#                 self.cursor.execute(query, (
#                     item['titre'], item['date'], item['duree'], item['genre'], item['realisateur'], item['distributeur'],
#                     item['nationalites'], item['langue_d_origine'], item['type_film'],
#                     item['annee_production'], 
#                     item['nombre_article'], item['description'], item['film_id_allocine'], item['image']
#                 ))
#                 self.conn.commit()
#                 film_id = self.cursor.execute("SELECT @@IDENTITY").fetchone()[0]
                
#             except Exception as e:
#                 # En cas d'erreur lors de l'insertion, vous pouvez choisir de supprimer l'item ou de le logger
#                 raise DropItem(f'Erreur lors de l\'insertion des données dans la base de données films : {e}')

#             try:
#                 # Insérer les acteurs dans la table "acteurs_films" en les associant avec l'ID du film
#                 for acteur in item['acteurs']:
#                     acteur_query = '''
#                     INSERT INTO acteurs_films (film_id, acteurs)
#                     VALUES (?, ?);
#                     '''
#                     self.cursor.execute(acteur_query, (film_id, acteur))
#                     self.conn.commit()
#             except Exception as e:
#                 # En cas d'erreur lors de l'insertion, vous pouvez choisir de supprimer l'item ou de le logger
#                 raise DropItem(f'Erreur lors de l\'insertion des données dans la base de données acteurs : {e}')
        
#         if spider.name == 'top_acteurs_spider':
#             try:
#                 # Insérer les acteurs dans la table "top_acteur"
#                 for acteur in item['acteur']:
#                     acteur_query = '''
#                     INSERT INTO top_acteur (acteur)
#                     VALUES (?);
#                     '''
#                     self.cursor.execute(acteur_query, (acteur,))
#                     self.conn.commit()

#             except Exception as e:
#             # En cas d'erreur lors de l'insertion, vous pouvez choisir de supprimer l'item ou de le logger
#                 raise DropItem(f'Erreur lors de l\'insertion des données dans la base de données acteurs : {e}')

#         if spider.name == 'boxoffice_spider':
#             try:
#                 # Récupérer l'ID du film à partir de la table "films" en utilisant le champ "film_id_allocine"
#                 select_film_id_query = '''
#                 SELECT id FROM films WHERE film_id_allocine = ?;
#                 '''
#                 self.cursor.execute(select_film_id_query, (item['film_id_allocine'],))
#                 film_id_row = self.cursor.fetchone()  # Récupérer la première ligne
                
#                 if film_id_row:
#                     film_id = film_id_row[0]  # Récupérer l'ID du film à partir de la première colonne
#                     # Insérer les données dans la table "boxoffice" en utilisant l'ID du film
#                     query = '''
#                     INSERT INTO boxoffice (titre, fin_semaine_1, boxoffice_1, boxoffice_2, film_id_allocine, film_id)
#                     VALUES (?, ?, ?, ?, ?, ?);
#                     '''
#                     self.cursor.execute(query, (
#                         item['titre'], item['fin_semaine_1'], item['boxoffice_1'], item['boxoffice_2'], item['film_id_allocine'], film_id
#                     ))
#                     self.conn.commit()
#                 else:
#                     raise DropItem(f'Film avec film_id_allocine {item["film_id_allocine"]} non trouvé dans la base de données films')
                
#             except Exception as e:
#                 # En cas d'erreur lors de l'insertion, vous pouvez choisir de supprimer l'item ou de le logger
#                 raise DropItem(f'Erreur lors de l\'insertion des données dans la base de données boxoffice : {e}')

        
#         return item



