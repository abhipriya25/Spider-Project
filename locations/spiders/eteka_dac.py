# -*- coding: utf-8 -*-

import scrapy
from locations.items import GeojsonPointItem
from locations.categories import Code
import pycountry

class EtekaSpider(scrapy.Spider):
    
    name = "eteka_dac"
    brand_name = "ETEKA"
    spider_type = "chain"
    spider_chain_id = 1009
    spider_categories = [Code.PETROL_GASOLINE_STATION]
    spider_countries = [pycountry.countries.lookup('gr').alpha_3]
    allowed_domains = ["eteka.com.gr"]
    
    start_urls = ["https://eteka.com.gr/wp-json/wpgmza/v1/features/base64eJyrVkrLzClJLVKyUqqOUcpNLIjPTIlRsopRMoxR0gEJFGeUFni6FAPFomOBAsmlxSX5uW6ZqTkpELFapVoABU0Wug"]

    def parse(self, response):
        '''
        @url https://eteka.com.gr/wp-json/wpgmza/v1/features/base64eJyrVkrLzClJLVKyUqqOUcpNLIjPTIlRsopRMoxR0gEJFGeUFni6FAPFomOBAsmlxSX5uW6ZqTkpELFapVoABU0Wug
        @returns items 220 230
        @scrapes ref name addr_full phone website lat lon
        '''

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
                'ref': row['id'],
                'chain_id': "1009",
                'chain_name': "ETEKA",
                'name': name,
                'addr_full': row['address'],
                'phone': [phone],
                'website': 'https://eteka.com.gr/',
                'lat': float(lat),
                'lon': float(lon)
            }

            yield GeojsonPointItem(**data)