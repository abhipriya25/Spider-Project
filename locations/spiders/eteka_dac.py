# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict

class EtekaSpider(scrapy.Spider):
    name: str = 'eteka_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.PETROL_GASOLINE_STATION]
    spider_countries: List[str] = [pycountry.countries.lookup('gr').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'ETEKA'}
    allowed_domains: List[str] = ['eteka.com.gr']

    def start_requests(self):
        url: str = "https://eteka.com.gr/wp-json/wpgmza/v1/features/base64eJyrVkrLzClJLVKyUqqOUcpNLIjPTIlRsopRMoxR0gEJFGeUFni6FAPFomOBAsmlxSX5uW6ZqTkpELFapVoABU0Wug"
        
        yield scrapy.Request(
            url=url,
        )


    def parse(self, response):
        responseData = response.json()['markers']
        for row in responseData:
            namePhone = row['title'].replace('<b>','').replace('</b>','')
            namePhone = namePhone.split('<br/>')
            name = namePhone[0]
            try:
                phone = namePhone[1].replace(' ', '').replace('Τηλ:', '')
            except:
                phone = ''
            
            lat = row['lat'].replace(' ', '')
            lon = row['lng'].replace(' ', '')
            if lat == 'Ν/Α':
                lat = 0
                lon = 0
            else:
                latSpl = lat.split('.')
                if len(latSpl) > 2:
                    lat = f'{latSpl[0]}.{latSpl[1]}{latSpl[2]}'
                lonSpl = lon.split('.')
                if len(lonSpl) > 2:
                    lon = f'{lonSpl[0]}.{lonSpl[1]}{lonSpl[2]}'
                
            
            data = {
                'ref': int(row['id']),
                'name': name,
                'brand': 'ETEKA',
                'addr_full': row['address'],
                'phone': phone,
                'website': 'https://eteka.com.gr/',
                'lat': float(lat),
                'lon': float(lon)
            }

            yield GeojsonPointItem(**data)