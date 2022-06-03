# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict

class DEIBlueSpider(scrapy.Spider):
    name: str = 'deiblue_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.EV_CHARGING_STATION]
    spider_countries: List[str] = [pycountry.countries.lookup('gr').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'DEI Blue'}
    allowed_domains: List[str] = ['deiblue.com']

    def start_requests(self):
        url: str = "https://www.deiblue.com/main_service/api/infoinit/charging-locations"
        headers = {
            'Host': 'www.deiblue.com',
            'Accept': 'application/json, text/plain, */*',
            'CAPIKEY': 'fdgdaskgjn;ljnouin;dfasljdofiasiofsnglsadnglnx',
            'Referer': 'https://www.deiblue.com/location',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'
        }
        yield scrapy.Request(
            url=url,
            headers=headers
        )


    def parse(self, response):
        responseData = response.json()['Data']['ChargingPoints']

        for i, row in enumerate(responseData):
            data = {
                'ref': int(i),
                'name': row['Title'],
                'brand': 'DEI Blue',
                'street': row['Address'],
                'website': 'https://deiblue.com/',
                'lat': float(row['X']),
                'lon': float(row['Y']),
            }

            yield GeojsonPointItem(**data)