# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy

class AllocineBoxofficeItem(scrapy.Item):
    titre = scrapy.Field()
    boxoffice_1 = scrapy.Field()
    boxoffice_2 = scrapy.Field()
    fin_semaine_1 = scrapy.Field()
    film_id = scrapy.Field()
    
class AllocineFilmsItem(scrapy.Item):
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
    nombre_article = scrapy.Field()
    recompenses = scrapy.Field()
    distributeur = scrapy.Field()
    film_id = scrapy.Field()
