# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict

class BP_GB_IE_Spider(scrapy.Spider):

    name = "bp_gb_ie_dac"
    brand_name = "BP Oil"
    spider_type: str = "chain"
    spider_chain_id = 7
    spider_chain_name = "BP"
    spider_categories: List[str] = [Code.PETROL_GASOLINE_STATION]
    spider_countries: List[str] = [pycountry.countries.lookup('gb').alpha_2, pycountry.countries.lookup('ie').alpha_2]
    allowed_domains: List[str] = ['www.bp.com','bpretaillocator.geoapp.me']

    area_bounds = {
        'sw' : [49.9, -21.3],
        'ne' : [60.6, 2.3]
    }

    def start_requests(self):

        sw = self.area_bounds['sw']
        ne = self.area_bounds['ne']

        st_url = f'https://bpretaillocator.geoapp.me/api/v1/locations/within_bounds?sw%5B%5D={str(sw[0])}&sw%5B%5D={str(sw[1])}&ne%5B%5D={str(ne[0])}&ne%5B%5D={str(ne[1])}&format=json'

        yield scrapy.Request(
            url=st_url,
            method='GET',
            callback=self.val_data,
        )

    def val_data(self, response):

        data = response.json()

        for elem in data:

            if elem.get("centroid") != None:

                sw = elem['bounds']['sw']
                ne = elem['bounds']['ne']

                link = f'https://bpretaillocator.geoapp.me/api/v1/locations/within_bounds?sw%5B%5D={str(sw[0])}&sw%5B%5D={str(sw[1])}&ne%5B%5D={str(ne[0])}&ne%5B%5D={str(ne[1])}&format=json'

                yield scrapy.Request(
                    url=link, 
                    dont_filter=True,
                    method='GET', 
                    callback=self.val_data
                )

        for item in list(self.parse(response)):
            yield item

    def parse_hours(self, row):

        days = {
            'Mon' : 'Mo', 
            'Tue' : 'Tu',
            'Wed' : 'We',
            'Thu' : 'Th',
            'Fri' : 'Fr',
            'Sat' : 'Sa',
            'Sun' : 'Su',
        }

        opening = ''

        if row != []:

            for el in row:
                opening += f"{el['days'][0]}-{el['days'][len(el['days']) - 1]} {el['hours'][0][0]}-{el['hours'][0][1]}; "

            for i, j in days.items():
                opening = opening.replace(i, j)

        return opening[:-2]

    def parse(self, response):

        responseData = response.json()

        for row in responseData:

            if row.get("country_code") in self.spider_countries:

                data = {
                    'ref': row.get('id'),
                    'chain_name': self.spider_chain_name,
                    'chain_id': self.spider_chain_id,
                    'brand': self.brand_name,
                    'name': row.get('name'),
                    'street': row.get('address'),
                    'city': row.get('city'),
                    'country': row.get('country_code'),
                    'postcode': row.get('postcode'),
                    'phone': row.get('telephone'),
                    'website': 'https://www.bp.com/en_gb/united-kingdom/home',
                    'opening_hours': self.parse_hours(row.get('opening_hours')),
                    'lat': float(row.get('lat')),
                    'lon': float(row.get('lng')),
                }

                yield GeojsonPointItem(**data)