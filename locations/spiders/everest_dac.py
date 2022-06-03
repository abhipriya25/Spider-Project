# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict

class EverestSpider(scrapy.Spider):
    name: str = 'everest_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.CAFETERIA, Code.FAST_FOOD]
    spider_countries: List[str] = [pycountry.countries.lookup('gr').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'Everest'}
    allowed_domains: List[str] = ['everest.gr']

    def start_requests(self):
        url = 'https://www.everest.gr/ajax/Atcom.Sites.Everest.Components.StoreFinder.GetStores/'
        
        yield scrapy.Request(
            url=url,
            method='POST'
        )
    
    def parse(self, response):
        '''
            Request returns a json with all data for each store
            Returns 105 features (2022-05-30)
        '''
        responseData = response.json()['results']
        for row in responseData:
            data = {
                'ref': row['ID'],
                'name': row['Name'],
                'brand': 'EVEREST',
                'website': 'https://www.everest.gr/',
                'addr_full': row['Address'],
                'phone': row['PhoneNumber'],
                'lon': row['Lng'],
                'lat': row['Lat']
            }

     

            yield GeojsonPointItem(**data)