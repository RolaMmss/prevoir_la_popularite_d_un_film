import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import AllocineMovieItem
import scrapy

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import AllocineMovieItem

class AllocineSpiderSpider(CrawlSpider):
    name = "allocine_spider"
    allowed_domains = ["allocine.fr"]
    start_urls = ["https://www.allocine.fr/boxoffice/france/sem-2023-04-19/"]

    rules = (
        Rule(LinkExtractor(restrict_css=".meta-title-link"), callback="parse_movie_details"),
    )

    # Spécifiez les colonnes pour le CSV
    fields = ['title', 'date', 'boxoffice']
    
    def parse_start_url(self, response):
        boxoffice = response.css('strong::text').get()

        allocine_movies_items = AllocineMovieItem()
        allocine_movies_items['title'] = None
        allocine_movies_items['date'] = None
        allocine_movies_items['boxoffice'] = boxoffice

        yield allocine_movies_items

    def parse_movie_details(self, response):
        title = response.css('div.titlebar-title.titlebar-title-lg::text').get()
        date = response.css('a.xXx.date.blue-link::text').get()
        boxoffice = response.css('strong::text').get()

        allocine_movies_items = AllocineMovieItem()
        allocine_movies_items['title'] = title
        allocine_movies_items['date'] = date
        allocine_movies_items['boxoffice'] = boxoffice
    
        yield allocine_movies_items
