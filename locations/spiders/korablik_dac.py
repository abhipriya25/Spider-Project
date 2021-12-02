# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem
from scrapy.http import Request, HtmlResponse
import re

class KorablikSpider(scrapy.Spider):
    name = 'korablik_dac'
    allowed_domains = ['korablik.ru']
    start_urls = ['https://voronezh.korablik.ru/shops/ajax.php?city=']

    def parse(self, response: HtmlResponse):
        data = response.json()
        print()
        item = GeojsonPointItem()

        item['ref'] = 1
        item['lat'] = lat
        item['lon'] = lng
        item['name'] = name
        item['country'] = 'Serbia'
        item['street'] = street
        item['opening_hours'] = open_hours
        item['housenumber'] = housenum
        item['addr_full'] = addr
        item['website'] = 'https://promenadanovisad.rs/'
        item['email'] = mail

        yield item