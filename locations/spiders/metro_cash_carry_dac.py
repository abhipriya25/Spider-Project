# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict
from bs4 import BeautifulSoup

class MetroCashCarrySpider(scrapy.Spider):
    name: str = 'metro_cash_carry_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.MARKET]
    spider_countries: List[str] = [pycountry.countries.lookup('gr').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'Metro Cash & Carry'}
    allowed_domains: List[str] = ['metrocashandcarry.gr']

    def start_requests(self):
        url = 'https://www.metrocashandcarry.gr/Katastimata/Evresi-plisiesterou'

        yield scrapy.Request(
            url=url
        )
    
    def parse(self, response):
        '''
            Features 49 (2022-06-09)
        '''
        doc = BeautifulSoup(response.text)
        boxes = doc.find_all(class_='store box')

        for box in boxes:
            data = {
                'ref': box.find(class_='maptitleinner').text,
                'name': box.find(class_='maptitleinner').text,
                'street': box.find(class_='mapadresspin').text,
                'brand': 'Metro Cash & Carry',
                'website': 'https://www.metrocashandcarry.gr/',
                'phone': box.find(class_='phonepin').text,
                'email': box.find(class_='emailpin').text,
                'opening_hours': 'Mo-Fr 06:00-21:00; Sa 06:00-20:00',
                'lat': box['data-latitude'],
                'lon': box['data-longitude']
            }
            yield GeojsonPointItem(**data)