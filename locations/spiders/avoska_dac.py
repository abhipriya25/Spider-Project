# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem


class AvoskaSpider(scrapy.Spider):
    name = 'avoska_dac'
    allowed_domains = ['avoska.ru']
    start_urls = ['https://avoska.ru/api/get_shops.php?map=1']

    def parse(self, response):
        data = response.json()

        for row in data['features']:
            item = GeojsonPointItem()

            item['ref'] = row['id']
            item['brand'] = 'Avoska'
            item['addr_full'] = row['properties']['hintContent']
            item['country'] = 'Russia'
            item['phone'] = '74956567022|74957254154'
            item['website'] = 'https://avoska.ru/'
            item['email'] = 'info@avoska.ru'
            item['lat'] = float(row['geometry']['coordinates'][0])
            item['lon'] = float(row['geometry']['coordinates'][1])

            yield item