# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict
import re

class Cobasi_BR_Spider(scrapy.Spider):

    name = "cobasi_br_dac"
    brand_name = "Cobasi"
    spider_type: str = "chain"
    spider_chain_id = 34020
    spider_chain_name = "Cobasi"
    spider_categories: List[str] = [Code.PET_SUPPLY]
    spider_countries: List[str] = [pycountry.countries.lookup('br').alpha_2]
    allowed_domains: List[str] = ['www.cobasi.com.br','lojas-api.cobasi.com.br']

    start_urls = ['https://lojas-api.cobasi.com.br/api/lojas']

    def parse_hours(self,row):
        
        opening = ''
        
        days = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
        month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jul', 'Jun', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        if row['weekdays'] != []:
            opening += f"{days[0]}-{days[4]} {row['weekdays'][0]['start']['hour']}:{row['weekdays'][0]['start']['minute']}-{row['weekdays'][0]['end']['hour']}:{row['weekdays'][0]['end']['minute']}; "
                    
        if row['saturday'] != []:
            opening += f"{days[5]} {row['saturday'][0]['start']['hour']}:{row['saturday'][0]['start']['minute']}-{row['saturday'][0]['end']['hour']}:{row['saturday'][0]['end']['minute']}; "
        
        if row['sunday'] != []:
            opening += f"{days[6]} {row['sunday'][0]['start']['hour']}:{row['sunday'][0]['start']['minute']}-{row['sunday'][0]['end']['hour']}:{row['sunday'][0]['end']['minute']}; "
                    
        if row['holidays'] != []:
            
            if len(row['holidays']) > 2:
                for j in row['holidays']:    
                     opening += f"{month[j['month']-1]} {j['day']} PH {j['hours'][0]['start']['hour']}:{j['hours'][0]['start']['minute']}-{j['hours'][0]['end']['hour']}:{j['hours'][0]['end']['minute']}; "
            else:
                opening += f"PH {row['holidays'][0]['start']['hour']}:{row['holidays'][0]['start']['minute']}-{row['holidays'][0]['end']['hour']}:{row['holidays'][0]['end']['minute']}; "
                        
        return opening[:-2]

    def parse(self, response):

        responseData = response.json()

        for row in responseData:
    
            data = {
                'ref': row.get('_id'),
                'chain_name': self.spider_chain_name,
                'chain_id': self.spider_chain_id,
                'brand': self.brand_name,
                'name': row.get('name'),
                'street': row.get('address'),
                'city': row.get('city'),
                'state': row.get('state'),
                'postcode': row.get('zipcode'),
                'country': self.spider_countries,
                'housenumber': row.get('number'),
                'phone': row.get('shopPhone'),
                'website': 'https://www.cobasi.com.br',
                'opening_hours': self.parse_hours(row.get('storeHours')),
                'lat': float(row.get('lat')),
                'lon': float(row.get('lng')),
            }

            yield GeojsonPointItem(**data)