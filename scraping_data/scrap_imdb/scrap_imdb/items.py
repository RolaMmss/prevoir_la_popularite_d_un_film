# Define here the models for your scraped items
import scrapy



class ScrapImdbItem(scrapy.Item):
    titre_original = scrapy.Field()
    durée = scrapy.Field()
    date = scrapy.Field()
    score = scrapy.Field()
    nbr_votants = scrapy.Field()
    desciption = scrapy.Field()
    genre = scrapy.Field()
    acteurs = scrapy.Field()
    pays = scrapy.Field()
    langue_d_origine = scrapy.Field()
    budget = scrapy.Field()
    Sociétés_de_production = scrapy.Field()
