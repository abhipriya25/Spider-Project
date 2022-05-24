# -*- coding: utf-8 -*-

import scrapy
import pycountry
import json
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict

class InchargeSpider(scrapy.Spider):
    name: str = 'incharge_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.EV_CHARGING_STATION]
    spider_countries: List[str] = [pycountry.countries.lookup('gr').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'Incharge NRG'}
    allowed_domains: List[str] = ['nrgincharge.gr']

    def start_requests(self):
        url: str = "https://www.nrgincharge.gr/sites/default/files/js/js_qTc9VQv6ecGpE9AuYfC6zfNFoWjCQYqqQ9Q2N8oSgX8.js"

        yield scrapy.Request(
            url=url
        )


    def parse(self, response):
        js = response.text
        js = ' '.join(js.split()) # Remove tabs, lines
        js = js.split('chargers: ')[1]
        js = js.split(']')[0]
        js += ']'
        js = js.replace('"', '') # Remove all " (we want to keep " only for keys and values)
        js = js.replace("\'", '"') 
        responseData = json.loads(js)

        for i, row in enumerate(responseData):
            data = {
                'ref': int(i),
                'name': row['name'],
                'brand': 'Incharge NRG',
                'addr_full': row['address'],
                'website': 'https://www.nrgincharge.gr',
                'lat': float(row['coords']['lat']),
                'lon': float(row['coords']['lng']),
            }

            yield GeojsonPointItem(**data)