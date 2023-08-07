import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import AllocineBoxofficeItem
from scrapy.settings import Settings

# Set the CSV file name and column order
CUSTOM_SETTINGS = {
    'FEED_FORMAT': 'csv',
    'FEED_URI': 'top_acteurs.csv',
    'FEED_EXPORT_FIELDS': ['acteur'],
    'MONGODB_COLLECTION': 'top_acteurs',
}



class BoxofficeSpider(CrawlSpider):
    name = "boxoffice_spider"
    custom_settings = CUSTOM_SETTINGS
    
    allowed_domains = ["allocine.fr"]
    
    DEPTH_LIMIT = 5

    # URL de la première page
    base_url = 'https://www.allocine.fr/personne/top/les-plus-vues/ever/'
    num_pages = 20

    def start_requests(self):
        for page in range(1, self.num_pages + 1):
            url = f"{self.base_url}?page={page}"
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # Extract the names of the most popular actors from the response
        #actors = response.css("a.meta-title-link::text").getall()
        actors = response.xpath('//a[@class="meta-title-link"]//text()').getall()

        for actor in actors:
            yield {'acteur': actor.strip()}

