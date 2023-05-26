# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict
import re

class Frango_Assado_BR_Spider(scrapy.Spider):

    name = "frango_assado_br_dac"
    brand_name = "Frango Assado"
    spider_type: str = "chain"
    spider_chain_id = 21136
    spider_chain_name = "Frango Assado"
    spider_categories: List[str] = [Code.FAST_FOOD]
    spider_countries: List[str] = [pycountry.countries.lookup('br').alpha_2]
    allowed_domains: List[str] = ['www.redefrangoassado.com.br']

    start_urls = ['https://www.redefrangoassado.com.br/wp-admin/admin-ajax.php?action=asl_load_stores&nonce=4319df701d&lang=&load_all=1&layout=1']

    def parse_hours(self, row):
        
        opening = ''
        
        del_word = ['Aberto','das','às','à']
        
        row = row.replace(':',' ')
        row = re.sub(r'\<[^>]*\>', '', row)
        row = re.sub(r'[A-Za-z]', ' ', row)
        
        k1 = row.split()
        
        m1 = []
        
        for s in k1:
            if s not in del_word:
                m1.append(s)
                
        if len(m1) == 1:
            opening += f'Mo-Su 00:00-23:59'
        
        elif len(m1) == 2:
            opening += f'Mo-Su {m1[0]}:00-{m1[1]}:00'
            
        else:
            opening += f'Mo-Su {m1[0]}:00-{m1[1]}:{m1[2]}'
        
        return opening

    def parse(self, response):

        responseData = response.json()

        for row in responseData:
    
            data = {
                'ref': row.get('id'),
                'chain_name': self.spider_chain_name,
                'chain_id': self.spider_chain_id,
                'brand': self.brand_name,
                'name': row.get('title'),
                'street': row.get('street'),
                'city': row.get('city'),
                'state': row.get('state'),
                'postcode': row.get('postal_code'),
                'country' : row.get('country'),
                'website': 'https://www.redefrangoassado.com.br',
                'opening_hours': self.parse_hours(row.get('description')),
                'lat': float(re.sub(r'--', '-', row.get('lat'))),
                'lon': float(re.sub(r'--', '-', row.get('lng'))),
            }

            yield GeojsonPointItem(**data)