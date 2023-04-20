# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict

class ElinSpider(scrapy.Spider):
    name = "elin_dac"
    brand_name = "Elin"
    spider_type = "chain"
    spider_chain_id = "1056"
    spider_categories = [Code.PETROL_GASOLINE_STATION]
    spider_countries = [pycountry.countries.lookup('gr').alpha_3]
    allowed_domains = ["elin.gr"]

    start_urls = ["https://elin.gr/umbraco/backoffice/MapMarkers/GetMapMarkers?language=el"]

    def parse(self, response):
        '''
        @url https://elin.gr/umbraco/backoffice/MapMarkers/GetMapMarkers?language=el
        @returns items 550 560
        @scrapes ref name addr_full phone website lat lon
        '''
        responseData = response.json()
        for row in responseData:
            data = {
                'ref': row['Id'],
                'name': row['Title'],
                'website': 'https://elin.gr',
                'addr_full': row['Address'],
                'phone': row['Phone'].split("&"),
                'lat': row['Latitude'],
                'lon': row['Longitude']
            }
       
            yield GeojsonPointItem(**data)