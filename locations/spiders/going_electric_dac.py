# -*- coding: utf-8 -*-
from aiohttp import payload
import scrapy
import json
import requests
from locations.items import GeojsonPointItem


class GoingElectricSpider(scrapy.Spider):
    name = 'going_electric_dac'
    allowed_domains = ['goingelectric.de']
    start_urls = ['https://api-test.goingelectric.de/chargepoints']


    def parse_data(self, response):
        data = response.json()

        for row in data['chargelocations']:
            item = GeojsonPointItem()
    
            item['ref'] = row['id']
            item['addr_full'] = row['address']['address']
            item['country'] = row['address']['country']
            item['city'] = row['address']['city']
            item['street'] = row['address']['street']
            item['postcode'] = row['address']['postcode']
            item['name'] = row['name']
            item['lat'] = row['coordinates']['lat']
            item['lon'] = row['coordinates']['lng']

            yield item

