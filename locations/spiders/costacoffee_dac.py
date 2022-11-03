# _*_ coding: utf-8 _*_

import scrapy
from locations.categories import Code
from locations.items import GeojsonPointItem
import pycountry
from typing import List
from uuid import uuid4


class CostaCoffeeSpider(scrapy.Spider):
    name = 'costacoffee_dac'
    brand_name = 'Costa Coffee'
    spider_type = 'chain'
    spider_categories: List[str] = [Code.BAKERY_AND_BAKED_GOODS_STORE]
    spider_countries: List[str] = [pycountry.countries.lookup('in').alpha_3]
    allowed_domains: List[str] = ['costacoffee.in/']

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
    def parse_contacts(self, response):
        '''
        Parse contact information: phone, email, fax, etc.
        '''

        email: List[str] = [
            response.xpath("/html/body/div[1]/div[1]/div/main/article/div/p[2]/a/text()").get()
        ]

        dataUrl: str = 'https://www.costacoffee.in/help-and-advice'

        yield scrapy.Request(
            dataUrl,
            callback=self.parse,
            cb_kwargs=dict(email=email, phone=phone)
        )


    def parse(self, response, email: List[str]):

        responseData = response.json()

        for row in responseData['items']:
            data = {
                'ref': str(uuid4()),
                'name': row.get('fields').get('storeName'),
                'addr_full': row.get('fields').get('storeAddress'),
                'website': 'costacoffee.in/',
                'email': email,
                'lat': float(row.get('fields').get('location').get('lat')),
                'lon': float(row.get('fields').get('location').get('lon')),
            }
            yield GeojsonPointItem(**data)

