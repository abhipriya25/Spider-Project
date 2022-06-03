# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict

class GoodysSpider(scrapy.Spider):
    name: str = 'goodys_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.FAST_FOOD, Code.RESTAURANT]
    spider_countries: List[str] = [pycountry.countries.lookup('gr').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'Goodys'}
    allowed_domains: List[str] = ['goodys.com']

    def start_requests(self):
        url: str = "https://www.goodys.com/ajax/Atcom.Sites.Goodys.Components.StoreFinder.GetStores/?method=TakeAway"
        
        yield scrapy.Request(
            url=url,
            method='POST'
        )


    def parse(self, response):
        responseData = response.json()['results']
        for row in responseData:
            r = row['StoreStateInfo']['StoreViewInfo']
            data = {
                'ref': r['ID'],
                'name': r['Name'],
                'brand': "Goody's",
                'addr_full': r['Address'],
                'postcode': r['ZipCode'],
                'phone': r['ContactPhone'],
                'website': 'https://www.goodys.com/',
                'lat': float(r['Lat']),
                'lon': float(r['Lng'])
            }

            yield GeojsonPointItem(**data)