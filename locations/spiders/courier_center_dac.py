# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict
import xmltodict

class CourierCenterSpider(scrapy.Spider):
    name: str = 'courier_center_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.COURIERS]
    spider_countries: List[str] = [pycountry.countries.lookup('gr').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'Courier Center'}
    allowed_domains: List[str] = ['courier.gr']

    def start_requests(self):
        url = 'https://www.courier.gr/physical/stores/markers/s/keq3ke43t6i0fml2jfh948q2l6'
        headers = {
            'cookie': "_ga=GA1.2.937987529.1653915050; frontend=keq3ke43t6i0fml2jfh948q2l6; frontend_cid=hKwylDNjv9bmQRzV; _gid=GA1.2.1944312492.1654165203; _gat_gtag_UA_1370150_52=1"
        }

        yield scrapy.Request(
            url=url,
            headers=headers
        )
    
    def parse(self, response):
        '''
            Returns 107 features (2022-06-01)
            Response is xml, we convert to dictionary
        '''

        markerDict = xmltodict.parse(response.text)
        resposeData = markerDict['markers']['marker']

        for row in resposeData:
            data = {
                'ref': row['@id'],
                'brand': 'Courier Center',
                'name': row['@name'],
                'addr_full': row['@address'],
                'phone': row['@phone'],
                'lat': float(row['@lat']),
                'lon': float(row['@lng'])
            }
        
            
            yield GeojsonPointItem(**data)