# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code


class DucatiSpider(scrapy.Spider):
    name = "ducati_dac"
    brand_name = "Ducati"
    spider_type = "chain"
    spider_chain_id = 23890
    spider_chain_name = "Ducati"
    spider_categories = [Code.MOTORCYCLE_DEALERSHIP, Code.BUSINESS_FACILITY]
    # spider_countries = [pycountry.countries.lookup('ind').alpha_3]
    allowed_domains = ["ducati.com"]

    start_urls = ["https://www.ducati.com/ww/en/api/dealers/markers?lat=51.165691&lng=10.451526&filters="]
  
    def parse(self, response):
        '''
        @url https://www.ducati.com/ww/en/api/dealers/markers?lat=51.165691&lng=10.451526&filters=
        @returns 765 775
        @scrapes ref website brand chain_name chain_id name addr_full email lat lon
        '''

        responseData = response.json()['results']
    
        for row in responseData:    

            data = {
                'ref': row['id'],
                'website': f'https://www.ducati.com/ww/en/dealers/{row["url"]}',
                'brand': 'Ducati',
                'chain_name': 'Ducati',
                'chain_id': 23890,
                'name': row['name'],
                'addr_full': row['address'],
                'email': row['mail'],
                'lat': float(row['lat']),
                'lon': float(row['lng']),
            }
            
            yield GeojsonPointItem(**data)