# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict

class SberbankOfficesSpider(scrapy.Spider):
    name: str = 'sberbank_offices_dac'
    spider_categories = [Code.BANK]
    spider_type: str = 'chain'
    item_attributes: Dict[str, str] = {'brand': 'Sberbank'}
    allowed_domains: List[str] = ['sb.k-safety.ru']
    

    def start_requests(self):
        '''
        Spider entrypoint. 
        Request chaining starts from here.
        '''
        url: str = "http://sb.k-safety.ru/vsp_here.json"
        
        yield scrapy.Request(
            url=url, 
            method='GET', 
            callback=self.parse
        )
    
    def parse_opening_hours(self, feature: dict):
        
        try:
            periods: List = feature['regularHours']['periods']
            return ";".join([f"{period['openDay']} {period['openTime']['hours']}:{period['openTime']['minutes']}-{period['closeTime']['hours']}:{period['closeTime']['minutes']}" for period in periods])
        except:
            return ""

    def parse(self, response):
        '''
        Parse data according to GeojsonPointItem schema.
        Possible attributes: DATA_FORMAT.md.
        Scrapy check docs: https://docs.scrapy.org/en/latest/topics/contracts.html.

        @url http://sb.k-safety.ru/vsp_here.json
        @returns items 12000 12600
        @returns requests 0 0
        
        @scrapes ref name city state addr_full website phone opening_hours lat lon 
        '''
        data = response.json()

        for row in data:
            
            data = {
                'ref': row['storeCode'],
                'name': row['locationName'],
                'city': row['address']['locality'],
                'state': row['address']['administrativeArea'],
                'addr_full': row['address']['addressLines'][0],
                'website': row['websiteUrl'],
                'phone': [row['primaryPhone']],
                'opening_hours': self.parse_opening_hours(row),
                'lat': row['latlng']['latitude'],
                'lon': row['latlng']['longitude'],
            }

            yield GeojsonPointItem(**data)