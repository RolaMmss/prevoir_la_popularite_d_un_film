# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapFilmsProchainementItem(scrapy.Item):
    titre = scrapy.Field()
    date = scrapy.Field()
    realisateur = scrapy.Field()
    duree = scrapy.Field()
    type_film = scrapy.Field()
    description = scrapy.Field()
    genre = scrapy.Field()
    acteurs = scrapy.Field()
    annee_production = scrapy.Field()
    langue_d_origine = scrapy.Field()
    nationalites = scrapy.Field()
    distributeur = scrapy.Field()
    film_id_allocine = scrapy.Field()
    image = scrapy.Field()
    

class BoxOfficeItem(scrapy.Item):
    film_id_allocine = scrapy.Field()
    boxoffice = scrapy.Field()
