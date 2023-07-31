# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter
import csv
import os
from .utils import convert_to_dd_mm_aaaa, convert_to_minutes
import re 
from .items import AllocineFilmsItem

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
        
        field_names = ['titre', 'date', 'genre', 'duree', 'realisateur', 'distributeur', 'acteurs',
                             'nationalites', 'langue_d_origine', 'type_film', 'annee_production','nombre_article', 
                             'recompenses', 'description']
                  
        ## Strip all whitspaces from strings and handle lists
        for field_name in field_names:
            value = adapter.get(field_name)
            if field_name is not isinstance(value, list):
                # Convert the value to a string if it's not already
                adapter[field_name] = str(value).strip()
        
        ## Process the date field
        date_value = adapter.get('date')
        adapter['date'] = convert_to_dd_mm_aaaa(date_value)
        
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
            genres_str = "_".join(genres)
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
            
            
        ## Process the acteurs field
        acteurs_value = adapter.get('acteurs')
        if acteurs_value is not None and isinstance(acteurs_value, str):
            acteurs = [acteurs.strip() for acteurs in acteurs_value.split(',')]
            # Join the acteurs list into a single string separated by underscores
            acteurs_str = "_".join(acteurs)
            # Remove quotes and brackets
            acteurs_str = re.sub(r"['\"\[\]]", "", acteurs_str)
            adapter['acteurs'] = acteurs_str
            
            
        return item

    
    

class BoxOfficePipeline:
    def process_item(self, item, spider):
        if 'fin_semaine_1' in item:
            fin_semaine_1 = item['fin_semaine_1']
            if 'au' in fin_semaine_1:
                _, date = fin_semaine_1.split('au')
                item['fin_semaine_1'] = convert_to_dd_mm_aaaa(date.strip())

        return item