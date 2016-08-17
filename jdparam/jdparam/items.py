# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdparamItem(scrapy.Item):
    sub_mobile_id = scrapy.Field()
    bodyinfos = scrapy.Field()
    base_info = scrapy.Field()
    mobile_os = scrapy.Field()
    mobile_cpu = scrapy.Field()
    mobile_internet = scrapy.Field()
    mobile_store = scrapy.Field()
    mobile_screen = scrapy.Field()
    front_camera = scrapy.Field()
    rear_camera = scrapy.Field()
    battery_info = scrapy.Field()
    data_interface = scrapy.Field()
    mobile_feature = scrapy.Field()
