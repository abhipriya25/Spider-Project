# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EdgarsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    opening_hours = scrapy.Field()
    name = scrapy.Field()
    store_url = scrapy.Field()
    addr_full = scrapy.Field()
    phone = scrapy.Field()
    pass
