# Define here the models for your scraped items
import scrapy



class ScrapImdbItem(scrapy.Item):
    titre = scrapy.Field()
    date = scrapy.Field()
    réalisateur = scrapy.Field()
    titre_original = scrapy.Field()
    durée = scrapy.Field()
    type_film = scrapy.Field()
    note_presse = scrapy.Field()
    note_spectateurs = scrapy.Field()
    description = scrapy.Field()
    genre = scrapy.Field()
    acteurs = scrapy.Field()
    annee_production = scrapy.Field()
    langue_d_origine = scrapy.Field()
    nationnalités = scrapy.Field()
    nombre_article = scrapy.Field()
    budget = scrapy.Field()
    recompenses = scrapy.Field()
 
