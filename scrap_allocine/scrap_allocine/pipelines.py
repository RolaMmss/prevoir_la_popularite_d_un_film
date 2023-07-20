# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
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


