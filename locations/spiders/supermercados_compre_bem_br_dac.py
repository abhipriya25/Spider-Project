# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict
import re

class Supermercados_Compre_Bem_br_Spider(scrapy.Spider):

    name = "supermercados_compre_bem_br_dac"
    brand_name = "Supermercados Compre Bem"
    spider_type: str = "chain"
    spider_chain_id = 4712
    spider_chain_name = "Supermercados Compre Bem"
    spider_categories: List[str] = [Code.GROCERY]
    spider_countries: List[str] = [pycountry.countries.lookup('br').alpha_2]
    allowed_domains: List[str] = ['comprebem.com.br','api.comprebem.com.br']

    start_urls = ['https://api.comprebem.com.br/store']

    def parse_hours(self, row):
        
        del_word = ['De','das','às','e', ',', 'a']
        
        days = {
            'segunda' : 'Mo',
            'Seg.' : 'Mo', 
            'Dom.' : 'Su',
            'sábado' : 'Sa',
            'Domingos' : 'Su',
            'domingo' : 'Su',
            'sáb.' : 'Sa',
            'feriados' : '',
            'feriado' : ''
        }
        
        r_normal = row['normal']
        r_special = row['special']
        
        for i, j in days.items():
            r_normal = r_normal.replace(i, j)
            
        for i, j in days.items():
             r_special = r_special.replace(i, j)
        
        r_normal = re.sub(r'[^\w\s]','', r_normal) 
        r_special = re.sub(r'[^\w\s]','', r_special) 
        
        k1 = r_normal.split()
        k2 = r_special.split()
        
        m1 = []
        m2 = []
        
        for s in k1:
            if s not in del_word:
                m1.append(s)
        
        for s in k2:
            if s not in del_word:
                m2.append(s)
            
        nums = re.findall(r'\d+', row['normal'])
        nums = [int(i) for i in nums]
        
        nums_s = re.findall(r'\d+', row['special'])
        nums_s = [int(i) for i in nums_s]
        
        opening = ''
        
        if m1 != []:
            
            opening += f"{m1[0]}-{m1[1]} {nums[0]}:00-{nums[1]}:00; "
            
        if m2 != []:
            
            opening += f"{m2[0]}, PH {nums_s[0]}:00-{nums_s[1]}:00; "
        
        return opening[:-2]

    def parse(self, response):

        responseData = response.json()

        for row in responseData['result']:
    
            data = {
                'ref': row.get('id'),
                'chain_name': self.spider_chain_name,
                'chain_id': self.spider_chain_id,
                'brand': self.brand_name,
                'name': row.get('name'),
                'addr_full': row.get('location').get('fullAddress'),
                'street': row.get('location').get('address'),
                'city': row.get('location').get('city'),
                'state': row.get('location').get('state'),
                'housenumber': row.get('location').get('number'),
                'phone': row.get('phone'),
                'country': self.spider_countries,
                'store_url': f'https://comprebem.com.br/ofertas/{row.get("slug")}',
                'website': 'https://comprebem.com.br',
                'opening_hours': self.parse_hours(row.get('businessHours')),
                'lat': float(row.get('location').get('lat')),
                'lon': float(row.get('location').get('lon')),
            }

            yield GeojsonPointItem(**data)