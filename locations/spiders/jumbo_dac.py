# -*- coding: utf-8 -*-

import scrapy
import pycountry
from bs4 import BeautifulSoup
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict

class JumboSpider(scrapy.Spider):
    name: str = 'jumbo_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.SPECIALTY_STORE]
    spider_countries: List[str] = [pycountry.countries.lookup('gr').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'Jumbo'}
    allowed_domains: List[str] = ['https://corporate.e-jumbo.gr/']

    def start_requests(self):
        url: str = "https://corporate.e-jumbo.gr/katastimata-jumbo/"
        
        yield scrapy.Request(
            url=url
        )


    def parse(self, response):
        doc = BeautifulSoup(response.text, 'html.parser')
        item0 = doc.find_all('li', class_='item0 odd first')
        item1 = doc.find_all('li', class_='item1 odd')
        item2 = doc.find_all('li', class_='item2 odd last')
        items = item0 + item1 + item2

        for i, item in enumerate(items):
            try:
                name = item.find('li', class_='name').text
            except:
                name = ''
            
            try:
                address = item.find('li', class_='address-one').text
            except:
                address = ''        
            
            try:
                phone = item.find('li', class_='phone').text.replace('Τηλέφωνο: ','')
            except:
                phone = ''
                       
            try:
                longitude = float(item.find('div', class_="box-info")['data-longitude'])
            except:
                longitude = 0
            
            try:
                latitude = float(item.find('div', class_="box-info")['data-latitude'])
            except:
                latitude = 0
            
            data = {
                'ref': int(i),
                'name': name,
                'addr_full': address,
                'phone': phone,
                'website': 'https://corporate.e-jumbo.gr/',
                'lon': longitude,
                'lat': latitude
            }

            yield GeojsonPointItem(**data)