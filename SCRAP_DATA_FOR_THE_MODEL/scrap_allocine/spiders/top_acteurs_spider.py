import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import ActorItem

# Set the CSV file name and column order
CUSTOM_SETTINGS = {
    'CSV_OUTPUT_FILE': 'top_acteur.csv',
    'CSV_FIELDS_TO_EXPORT': ['acteur' ],  
    'ITEM_PIPELINES': {
            'scrap_allocine.pipelines.CsvPipeline': 301,
            # 'scrap_allocine.pipelines.AzureSQLPipeline' : 400

        }}

class TopActeursSpider(CrawlSpider):
    
    name = "top_acteurs_spider"
    allowed_domains = ["allocine.fr"]
    start_urls = ['https://www.allocine.fr/personne/top/les-plus-vues/ever/']

    custom_settings = CUSTOM_SETTINGS

    allowed_domains = ["allocine.fr"]
    
    DEPTH_LIMIT = 5

    # URL de la première page
    base_url = 'https://www.allocine.fr/personne/top/les-plus-vues/ever/'
    num_pages = 20

    def start_requests(self):
        for page in range(1, self.num_pages + 1):
            url = f"{self.base_url}?page={page}"
            
            yield scrapy.Request(url, callback=self.parse_actor)
            
    def parse_actor(self, response):
        actors = response.xpath('//a[@class="meta-title-link"]//text()').getall()

        for actor in actors:
            item = ActorItem()
            item['acteur'] = actor.strip()
            yield item
