import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import AllocineMovieItem
import scrapy

class AllocineSpiderSpider(CrawlSpider):
    name = "allocine_spider"
    allowed_domains = ["allocine.fr"]
    start_urls = ["https://www.allocine.fr/boxoffice/france/sem-2023-04-19/"]

    rules = (
        Rule(LinkExtractor(restrict_css=".meta-title-link"), callback="parse_movie_details"),
    )

    # Spécifiez les colonnes pour le CSV
    fields = ['title', 'date']
    
    def start_requests(self):
        yield scrapy.Request(url='https://www.allocine.fr/boxoffice/france/sem-2023-04-19/')

    def parse_movie_details(self, response):
        title = response.css('div.titlebar-title.titlebar-title-lg::text').get()
        date = response.css('a.xXx.date.blue-link::text').get()

        allocine_movies_items = AllocineMovieItem()
        
        allocine_movies_items['title'] = title
        allocine_movies_items['date'] = date

    
            
        yield allocine_movies_items
