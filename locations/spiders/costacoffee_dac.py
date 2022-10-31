# _*_ coding: utf-8 _*_

import scrapy
from locations.categories import Code
from locations.items import GeojsonPointItem
import pycountry
from typing import List


class CostaCoffeeSpider(scrapy.Spider):
    name = 'costacoffee_dac'
    brand_name = 'Costa Coffee'
    spider_type = 'chain'
    spider_categories: List[str] = [Code.BAKERY_AND_BAKED_GOODS_STORE]
    spider_countries: List[str] = [pycountry.countries.lookup('in').alpha_3]
    allowed_domains: List[str] = ['costacoffee.in/']

    #start_urls = ["https://www.costacoffee.in/api/cf/?locale=en-IN&include=2&content_type=storeLocatorStore&limit=500&f\
    #ields.location[near]=28.553532369889,77.12456293893058"]

    def start_requests(self):
        url = "https://www.costacoffee.in/api/cf/?locale=en-IN&include=2&content_type=storeLocatorStore&limit=500&f\
    #ields.location[near]=28.553532369889,77.12456293893058"

        headers = {
            "lat": "28.553532369889",
            "lon": "77.12456293893058",
        }

        yield scrapy.Request(
            url=url,
            method='GET',
            headers=headers,
            # Response will be parsed in parse function
            callback=self.parse,
        )


    def parse(self, response):

        responseData = response.json()

        for row in responseData['items']:
            data = {
                'ref': row.get('fields').get('storeType').get('sys').get('id'),
                'name': row.get('fields').get('storeName'),
                'addr_full': row.get('fields').get('storeAddress'),
                'website': 'costacoffee.in/',
                'lat': float(row.get('fields').get('location').get('lat')),
                'lon': float(row.get('fields').get('location').get('lon')),
            }
            yield GeojsonPointItem(**data)

