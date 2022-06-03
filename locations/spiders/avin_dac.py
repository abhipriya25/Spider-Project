# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict

class AvinSpider(scrapy.Spider):
    name: str = 'avin_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.PETROL_GASOLINE_STATION]
    spider_countries: List[str] = [pycountry.countries.lookup('gr').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'Avin Oil'}
    allowed_domains: List[str] = ['avinoil.gr']

    def start_requests(self):
        url: str = "https://www.avinoil.gr/wp-content/plugins/bb-custom-gas-stations/gas-stations.json"
        
        yield scrapy.Request(
            url=url
        )


    def parse(self, response):
        responseData = response.json()
        for row in responseData:
            data = {
                'ref': row['id'],
                'name': row['title'],
                'brand': 'Avin Oil',
                'street': row['address'],
                'city': row['city'],
                'state': row['state'],
                'postcode': row['zip'],
                'phone': row['phone'],
                'website': 'https://www.avinoil.gr/',
                'lat': float(row['lat']),
                'lon': float(row['lng'])
            }

            yield GeojsonPointItem(**data)