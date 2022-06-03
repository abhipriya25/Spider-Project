# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict

class CoralEnergySpider(scrapy.Spider):
    name: str = 'coral_energy_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.PETROL_GASOLINE_STATION]
    spider_countries: List[str] = [pycountry.countries.lookup('gr').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'Shell'}
    allowed_domains: List[str] = ['coralenergy.gr']

    def start_requests(self):
        url: str = "https://www.coralenergy.gr/umbraco/api/NetworkDisplay/GetPoints/"
        headers = {
            'content-type': 'application/json; charset=UTF-8',
            'x-requested-with': 'XMLHttpRequest'
        }
        payload = "{\"Key\":3141}"
        yield scrapy.Request(
            url=url,
            headers=headers,
            body=payload,
            method='POST'
        )


    def parse(self, response):
        responseData = response.json()['points']

        for i, row in enumerate(responseData):      
            
            data = {
                'ref': int(i),
                'name': row['title'],
                'brand': 'Shell',
                'addr_full': row['address'],
                'website': 'https://www.coralenergy.gr/',
                'phone': row['telephones'],
                'lat': float(row['latitude']),
                'lon': float(row['longitude'])
            }

            yield GeojsonPointItem(**data)