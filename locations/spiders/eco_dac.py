# -*- coding: utf-8 -*-
import scrapy
import re
import json
from locations.items import GeojsonPointItem


class EcoSpider(scrapy.Spider):

    name = 'eco_dac'
    allowed_domains = ['eko.com.cy']
    start_urls = ['http://www.eko.com.cy/en/stations/katastimata/']


    def parse(self, response):
        data = response.css('div[class*="box-info"]') 
        i = 0
        # pipenv run scrapy crawl eco_dac --output=eco.geojson
        for row in data:
            item = GeojsonPointItem()
            
            item['name'] = row.css('div div[class*="name-container"] span *::text').get()
            item['ref'] = i
            item['brand'] = 'Eco'
            item['addr_full'] = row.css('li[class*="address-one"] *::text').get()
            item['phone'] = row.css('li[class*="phone"] *::text').get()
            item['website'] = 'http://www.eko.com.cy'
            item['email'] = 'EkoCustomerService@helpe.gr'
            item['lat'] = float(row.attrib['data-latitude'])
            item['lon'] = float(row.attrib['data-longitude'])
            i += 1
            yield item
