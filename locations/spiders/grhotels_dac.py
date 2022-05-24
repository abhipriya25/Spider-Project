# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict

class GRHotelsSpider(scrapy.Spider):
    name: str = 'grhotels_dac'
    spider_type: str = 'generic'
    spider_categories: List[str] = [Code.HOTEL]
    spider_countries: List[str] = [pycountry.countries.lookup('gr').alpha_2]
    allowed_domains: List[str] = ['grhotels.gr']

    def start_requests(self):
        url: str = "https://www.grhotels.gr/app/themes/grhotels/data-en.json"
        
        yield scrapy.Request(
            url=url
        )

    def parse(self, response):
        responseData = response.json()
        for row in responseData:
            data = {
                'ref': row['postid'],
                'name': row['title'],
                'addr_full': row['address'],
                'postcode': row['zipcode'],
                'phone': row['hotel_phone_number_1'],
                'website': row['hotel_website'],
                'email': row['hotel_email'],
                'lat': float(row['geometry']['coordinates'][0]),
                'lon': float(row['geometry']['coordinates'][1]),
            }

            yield GeojsonPointItem(**data)