# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem


class TatneftSpider(scrapy.Spider):
    name = 'tatneft_dac'
    allowed_domains = ['tatneft.ru']
    start_urls = ['https://api.gs.tatneft.ru/api/v2/azs/']

    def parse(self, response):
        data = response.json()

        for row in data['data']:
            item = GeojsonPointItem()

            item['ref'] = row['id']
            item['brand'] = 'Tatneft'
            item['addr_full'] = row['address']
            item['country'] = 'Russia'
            #item['phone'] = '74956567022|74957254154'
            item['website'] = 'https://tatneft.ru/'
            #item['email'] = 'info@avoska.ru'
            item['lat'] = float(row['lat'])
            item['lon'] = float(row['lon'])

            yield item