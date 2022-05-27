# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict

class MikelSpider(scrapy.Spider):
    name: str = 'mikel_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.CAFETERIA]
    spider_countries: List[str] = [pycountry.countries.lookup('gr').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'Mikel'}
    allowed_domains: List[str] = ['mikelcoffee.com']

    def start_requests(self):
        url = 'https://www.mikelcoffee.com/js/stores.json'
        
        yield scrapy.Request(
            url=url
        )
    
    def replace_all(self, text):
        rep = {
        'Monday': 'Mo', 'Tuesday': 'Tu', 'Wednesday': 'We', 'Thursday': 'Th', 'Friday': 'Fr', 'Saturday': 'Sa', 'Sunday': 'Su', ' - ':'-', ' -': '-', '- ': '-', ' &': '; ', '& ': '; ', '&': ';', ' :': ' ', ': ':' ', '  ':' ', 'Weekend': 'Sa-Su'
        }
        for i, j in rep.items():
            text = text.replace(i, j)
        return text


    def parse(self, response):
        '''
            The json has the stores divided per country, region, city
            Returns 313 features (2022-05-27)
        '''
        responseData = response.json()
        i=0
        lang = 'el' # Countries 0,1 have greek, others are in eng
        for j, country in enumerate(responseData):
            if j > 1:
                lang = 'en'
            for reg in country['regions']:
                for city in reg['cities']:
                    try:
                        cityName = city['name'][lang]
                    except: 
                        cityName = ''
                    for store in city['stores']:
                        coords = store['loc'].split(',')
                        lat = coords[0]
                        lon = coords[1]
                        data = {
                            'ref': int(i),
                            'addr_full': store['address'][lang],
                            'city': cityName,
                            'state': reg['name'][lang],
                            'country': country['name'][lang],
                            'opening_hours': self.replace_all(store['hours']['en']),
                            'brand': 'Mikel',
                            'website': 'https://www.mikelcoffee.com/',
                            'lat': float(lat),
                            'lon': float(lon)
                        }
                        i+=1
                        yield GeojsonPointItem(**data)