# -*- coding: utf-8 -*-

import scrapy
from locations.items import GeojsonPointItem
from locations.categories import Code
import pycountry

class AvinSpider(scrapy.Spider):
    name = "avin_dac"
    brand_name = "Avin"
    spider_type = "chain"
    spider_chain_id = "1004"
    spider_categories = [Code.PETROL_GASOLINE_STATION]
    spider_countries = [pycountry.countries.lookup('gr').alpha_3]
    allowed_domains = ["avinoil.gr"]

    start_urls = ["https://www.avinoil.gr/wp-content/plugins/bb-custom-gas-stations/gas-stations.json"]

    def parse(self, response):
        '''
        @url https://www.avinoil.gr/wp-content/plugins/bb-custom-gas-stations/gas-stations.json
        @returns items 500 520
        @scrapes ref name addr_full city state postcode phone website lat lon
        '''

        responseData = response.json()
        
        for row in responseData:
            data = {
                'ref': row['id'],
                'chain_name': 'Avin',
                'chain_id': '1004',
                'addr_full': row['address'],
                'city': row['city'],
                'state': row['state'],
                'postcode': row['zip'],
                'phone': [row['phone']],
                'website': 'https://www.avinoil.gr',
                'lat': float(row['lat']),
                'lon': float(row['lng'])
            }

            yield GeojsonPointItem(**data)