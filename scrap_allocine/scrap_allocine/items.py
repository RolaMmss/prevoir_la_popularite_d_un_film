# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# class AllocineMovieItem(scrapy.Item):
#     title = scrapy.Field()
#     boxoffice = scrapy.Field()

import scrapy

class AllocineMovieItem(scrapy.Item):
    title = scrapy.Field()
    boxoffice = scrapy.Field()
