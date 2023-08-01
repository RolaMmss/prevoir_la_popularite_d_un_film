# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter
import csv
from dotenv import load_dotenv
import os
import pypyodbc as odbc
import pyodbc
from scrapy.exceptions import DropItem




class CsvWriterPipeline:
    def __init__(self, csv_output_file):
        self.csv_output_file = csv_output_file

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        csv_output_file = settings.get('CSV_OUTPUT_FILE', 'items.csv')
        return cls(csv_output_file)

    def open_spider(self, spider):
        self.csv_file = open(self.csv_output_file, 'w', newline='', encoding='utf-8')
        self.csv_writer = csv.DictWriter(self.csv_file, fieldnames=spider.fields)
        self.csv_writer.writeheader()

    def close_spider(self, spider):
        self.csv_file.close()

    def process_item(self, item, spider):
        self.csv_writer.writerow(item)
        return item

from scrapy.exporters import CsvItemExporter
from pymongo import MongoClient
import os


class ScrapAllocinePipeline:

    def __init__(self, collection_name):
        load_dotenv()
        ATLAS_KEY = os.getenv('ATLAS_KEY')
        client = MongoClient(ATLAS_KEY, socketTimeoutMS=5000)
        db = client.allocine
        self.collection = db[collection_name]

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        collection_name = settings.get('MONGODB_COLLECTION', 'collection')
        return cls(collection_name)

    def process_item(self, item, spider):
        self.collection.insert_one(dict(item))
        return item




import os
from scrapy.exporters import CsvItemExporter

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



class AzureSQLPipeline:
    def __init__(self):
        load_dotenv()
        self.username = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.server = os.getenv('DB_SERVER')
        self.database = os.getenv('DB_name')
        self.DB_Driver = os.getenv('DB_Driver')

    def open_spider(self, spider):
        # Établir la connexion
        connection_string = f'Driver={self.DB_Driver};Server=tcp:{self.server},1433;Database={self.database};Uid={self.username};Pwd={self.password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
        
        self.conn = pyodbc.connect(connection_string)
        self.cursor = self.conn.cursor()


        # Delete les table s'il existent
        self.delete_table('acteurs_films')
        self.delete_table('films')

        # Créer la table "acteurs_films"
        create_acteurs_films_table_query = '''
        CREATE TABLE acteurs_films (
            id INT IDENTITY(1,1) PRIMARY KEY,
            film_id INT,
            acteurs VARCHAR(500)
        );
        '''
        self.cursor.execute(create_acteurs_films_table_query)
        self.conn.commit()

        
        # Créer la table "films"
        create_table_query = '''
        CREATE TABLE films (
            id INT IDENTITY(1,1) PRIMARY KEY,
            titre VARCHAR(500),
            date VARCHAR(500),
            durée VARCHAR(500),
            réalisateur VARCHAR(500),
            distributeur VARCHAR(500),
            titre_original VARCHAR(500),
            nationalités VARCHAR(500),
            langue_d_origine VARCHAR(500),
            type_film VARCHAR(500),
            annee_production VARCHAR(500),
            budget VARCHAR(500),
            note_presse VARCHAR(500),
            note_spectateurs VARCHAR(500),
            nombre_article VARCHAR(500),
            recompenses VARCHAR(500),
            description VARCHAR(2000)
        );
        '''
        self.cursor.execute(create_table_query)
        self.conn.commit()


    def delete_table(self, table_name):
        drop_table_query = f'DROP TABLE IF EXISTS {table_name};'
        self.cursor.execute(drop_table_query)
        self.conn.commit()


    def close_spider(self, spider):
        self.conn.close()
       



    def process_item(self, item, spider):
        try:
            query = '''
            INSERT INTO films (titre, date, durée, réalisateur, distributeur, titre_original, nationalités, langue_d_origine, type_film, annee_production, budget, note_presse, note_spectateurs, nombre_article, recompenses, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            '''
            self.cursor.execute(query, (
                item['titre'], item['date'], item['durée'], item['réalisateur'], item['distributeur'],
                item['titre_original'], item['nationalités'], item['langue_d_origine'], item['type_film'],
                item['annee_production'], item['budget'], item['note_presse'], item['note_spectateurs'],
                item['nombre_article'], item['recompenses'], item['description']
            ))
            self.conn.commit()
            film_id = self.cursor.execute("SELECT @@IDENTITY").fetchone()[0]


        except Exception as e:
            # En cas d'erreur lors de l'insertion, vous pouvez choisir de supprimer l'item ou de le logger
            raise DropItem(f'Erreur lors de l\'insertion des données dans la base de données films : {e}')
        
        try:

                # Insérer les acteurs dans la table "acteurs_films" en les associant avec l'ID du film
            for acteurs in item['acteurs']:
                acteur_query = '''
                INSERT INTO acteurs_films (film_id, acteurs)
                VALUES (?, ?);
                '''
                self.cursor.execute(acteur_query, (film_id, acteurs))
                self.conn.commit()
    
        except Exception as e:
            # En cas d'erreur lors de l'insertion, vous pouvez choisir de supprimer l'item ou de le logger
            raise DropItem(f'Erreur lors de l\'insertion des données dans la base de données acteurs : {e}')

        return item

