# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class JdBrandItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    link = scrapy.Field()


class JdModelItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()


class JdSubModelItem(scrapy.Item):
    brand_id = scrapy.Field()
    model_id = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
