import scrapy
from ..items import BoxOfficeItem
# Set the CSV file name and column order
CUSTOM_SETTINGS = {
    'CSV_OUTPUT_FILE': 'recent_boxoffice.csv',
    'CSV_FIELDS_TO_EXPORT': ['film_id_allocine', 'boxoffice'],  
    # 'ITEM_PIPELINES': {
    #         'scrap_allocine.pipelines.CsvPipeline': 301,
            
    #     }
    }

import scrapy
from ..items import BoxOfficeItem

class RecentBoxofficeSpider(scrapy.Spider):
    name = "recent_boxoffice_spider"
    allowed_domains = ["allocine.fr"]
    start_urls = ["https://www.allocine.fr/boxoffice/france/"]
    custom_settings = CUSTOM_SETTINGS


import scrapy
from ..items import BoxOfficeItem

class RecentBoxofficeSpider(scrapy.Spider):
    name = "recent_boxoffice_spider"
    allowed_domains = ["allocine.fr"]
    custom_settings = CUSTOM_SETTINGS
    start_urls = ["https://www.allocine.fr/boxoffice/france/"]

    def parse(self, response):
        items = BoxOfficeItem()

        film_id_links = response.css('h2.meta-title a::attr(href)').getall()
        film_ids = [link.split('=')[1].split('.')[0] for link in film_id_links]
        boxoffices = response.css('td[data-heading="Entrées"] strong::text').getall()
        weeks = response.css('td[data-heading="Semaine"]::text').getall()

        for film_id, boxoffice, week in zip(film_ids, boxoffices, weeks):
            if week == '\n1\n':
                items['film_id_allocine'] = film_id
                items['boxoffice'] = boxoffice
                yield items