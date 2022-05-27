# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict
from bs4 import BeautifulSoup

class CoffeeIslandSpider(scrapy.Spider):
    name: str = 'coffee_island_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.CAFETERIA]
    spider_countries: List[str] = [pycountry.countries.lookup('gr').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'Coffee Island'}
    allowed_domains: List[str] = ['coffeeisland.gr']

    def start_requests(self):
        url = 'https://www.coffeeisland.gr/stores/index'
        
        yield scrapy.Request(
            url=url
        )
    
    def parse(self, response):
        '''
            Returns 480 features (2022-05-27)
            Divs with class='popup-store-link' contain data for stores
        '''

        doc = BeautifulSoup(response.text)
        div = doc.find_all('div', class_='popup-store-link')
        for row in div:
            try:
                website = row.find('div', class_='font-1-1x font-weight-600 mb-2').find('a')['href']
            except:
                website = ''

            p = row.find('div', class_='d-block').find_all('p', class_='mb-2')
            
            # Opening hours
            op = p[1].text.split('takeaway: ')[1]
            if op != '-':
                op = op.replace(' - ', '-').replace(',', ';')
                op = f'Mo-Su {op}'
            else:
                op = ''
            
            try:
                phone = p[2].text
            except:
                pass
            data = {
                'ref': row['data-marker-id'],
                'brand': 'Coffee Island',
                'addr_full': p[0].text,
                'phone': phone,
                'website': website,
                'opening_hours': op,
                'lon': float(row['data-longitude']),
                'lat': float(row['data-latitude']),
            }

            yield GeojsonPointItem(**data)