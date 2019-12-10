# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AppstoreItem(scrapy.Item):
    
    date = scrapy.Field()
    subcategory = scrapy.Field()
    category = scrapy.Field()
    type = scrapy.Field()
    ranking = scrapy.Field()
    app_name = scrapy.Field()
    app_link = scrapy.Field()

    pass
