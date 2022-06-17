# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict

class OkMarketsGrSpider(scrapy.Spider):
    name: str = 'ok_markets_gr_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.MARKET]
    spider_countries: List[str] = [pycountry.countries.lookup('gr').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'OK Markets'}
    allowed_domains: List[str] = ['okmarkets.gr']

    def start_requests(self):
        url = 'https://www.okmarkets.gr/wp-admin/admin-ajax.php?action=store_search&lat=37.98381&lng=23.727539&max_results=1000&search_radius=10000&filter=237&autoload=1'

        yield scrapy.Request(
            url=url
        )
    
    def parse(self, response):
        '''
        127 Features (2022-06-08)
        '''
        responseData = response.json()

        # Opening hours is the same for all
        opening = 'Mo-Su 08:00-23:00'

        for row in responseData:
            # Parse data
            data = {
                'ref': row['id'],
                'name': row['store'],
                'brand': 'OK Markets',
                'website': 'https://www.okmarkets.gr/',
                'street': row['address'],
                'city': row['city'],
                'postcode': row['zip'],
                'phone': row['phone'],
                'opening_hours': opening,
                'lat': float(row['lat']),
                'lon': float(row['lng']),
            }
            yield GeojsonPointItem(**data)