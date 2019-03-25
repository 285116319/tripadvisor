# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhangzeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()

class ZhangzeGNItem(scrapy.Item):
    name= scrapy.Field()
    ImgUrl = scrapy.Field()

class Travel(scrapy.Item):
    date = scrapy.Field()

    location = scrapy.Field()  
    text = scrapy.Field()

    
class travelItems(scrapy.Item):
    number = scrapy.Field()
    name = scrapy.Field()
    maxpage = scrapy.Field()