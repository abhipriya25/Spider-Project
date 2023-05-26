# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict

class Shell_SWE_Spider(scrapy.Spider):

    name = "shell_swe_dac"
    brand_name = "Shell"
    spider_type: str = "chain"
    spider_chain_id = 10
    spider_chain_name = "Shell"
    spider_categories: List[str] = [Code.PETROL_GASOLINE_STATION]
    spider_countries: List[str] = [pycountry.countries.lookup('se').alpha_2]
    allowed_domains: List[str] = ['www.shell.se','shellfleetlocator.geoapp.me']

    area_bounds = {
        'sw' : [54.509945, 5.326009],
        'ne' : [69.089841, 32.143370]
    }

    def start_requests(self):

        sw = self.area_bounds['sw']
        ne = self.area_bounds['ne']

        st_url = f'https://shellfleetlocator.geoapp.me/api/v1/cf/locations/within_bounds?sw%5B%5D={str(sw[0])}&sw%5B%5D={str(sw[1])}&ne%5B%5D={str(ne[0])}&ne%5B%5D={str(ne[1])}&format=json';

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

                link = f'https://shellfleetlocator.geoapp.me/api/v1/cf/locations/within_bounds?sw%5B%5D={str(sw[0])}&sw%5B%5D={str(sw[1])}&ne%5B%5D={str(ne[0])}&ne%5B%5D={str(ne[1])}&format=json';

                yield scrapy.Request(
                    url=link,
                    method='GET',
                    dont_filter=True,
                    callback=self.val_data,
                )

        for item in list(self.get_item(response)):
            yield item     

    def get_item(self, response):

        responseData = response.json()

        for row in responseData:

            if row.get("country_code") in self.spider_countries and row.get('id').find('TPN') == -1:

                link = f'https://shellfleetlocator.geoapp.me/api/v1/cf/locations/{row["id"]}'

                yield scrapy.Request(
                    url=link,
                    method='GET',
                    dont_filter=True,
                    callback=self.parse,
                )

    def parse_hours(self, op, row):

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

        if op == "twenty_four_hour":
            opening += "Mo-Su 00:00-23:59; "
        else:
            if row != []:

                for el in row:
                    opening += f"{el['days'][0]}-{el['days'][len(el['days']) - 1]} {el['hours'][0][0]}-{el['hours'][0][1]}; "

                for i, j in days.items():
                    opening = opening.replace(i, j)

        return opening[:-2]

    def parse(self, response):

        row = response.json()

        data = {
            'ref': row.get('id'),
            'chain_name': self.spider_chain_name,
            'chain_id': self.spider_chain_id,
            'brand': self.brand_name,
            'name': row.get('name'),
            'street': row.get('address'),
            'city': row.get('city'),
            'country': row.get('country'),
            'postcode': row.get('postcode'),
            'phone': row.get('telephone'),
            'website': "https://www.shell.se",
            'store_url': row.get('website_url'),
            'opening_hours': self.parse_hours(row.get("open_status"), row.get('opening_hours')),
            'lat': float(row.get('lat')),
            'lon': float(row.get('lng')),
        }
            
        yield GeojsonPointItem(**data)