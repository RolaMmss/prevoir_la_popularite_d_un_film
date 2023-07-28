# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter
import csv
import csv

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
from dotenv import load_dotenv
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
