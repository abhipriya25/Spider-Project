# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict
import xmltodict
import pdb

class CourierCenterSpider(scrapy.Spider):
    name: str = 'courier_center_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.COURIERS]
    spider_countries: List[str] = [pycountry.countries.lookup('gr').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'Courier Center'}
    allowed_domains: List[str] = ['courier.gr']

    def start_requests(self):
        url = 'https://www.courier.gr/physical/stores/markers/s/u1b515mvgfffmcana91p19oph5'
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': '_ga=GA1.2.937987529.1653915050; frontend=u1b515mvgfffmcana91p19oph5; frontend_cid=IeWb589vJH7sFb6Q; _gid=GA1.2.1304927387.1655460772; _gat_gtag_UA_1370150_52=1; frontend=u1b515mvgfffmcana91p19oph5; frontend_cid=rvOLLftErT40tRnU',
            'referer': 'https://www.courier.gr/physical/stores/',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
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
        #pdb.set_trace()
        print(response.text)
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