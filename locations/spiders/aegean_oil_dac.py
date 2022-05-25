# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict

class AegeanOilSpider(scrapy.Spider):
    name: str = 'aegean_oil_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.PETROL_GASOLINE_STATION]
    spider_countries: List[str] = [pycountry.countries.lookup('gr').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'Aegean Oil'}
    allowed_domains: List[str] = ['aegeanoil.com']

    def start_requests(self):
        url: str = "https://aegeanoil.com/wp-content/themes/aegeanoil/station_data.json"
        
        yield scrapy.Request(
            url=url,
        )


    def parse(self, response):
        responseData = response.json()['json']

        for row in responseData:
            # Try to get phone
            try:
                phone = row['ΤΗΛΕΦΩΝΟ']
            except:
                phone = ''

            # Fix opening hours
            op_hours = ''
            days = ['ΩΡΑΡΙΟ ΔΕΥΤΕΡΑ', 'ΩΡΑΡΙΟ ΤΡΙΤΗ', 'ΩΡΑΡΙΟ ΤΕΤΑΡΤΗ', 
            'ΩΡΑΡΙΟ ΠΕΜΠΤΗ', 'ΩΡΑΡΙΟ ΠΑΡΑΣΚΕΥΗ', 'ΩΡΑΡΙΟ ΣΑΒΒΑΤΟ', 'ΩΡΑΡΙΟ ΚΥΡΙΑΚΗ']
            if 'ΩΡΑΡΙΟ ΔΕΥΤΕΡΑ' in row.keys():
                osm_days = ['Mo', 'Tu', "We", "Th", 'Fr', 'Sa', 'Su']
                for i in range(7):
                    hours = row[days[i]]
                    hours = hours.replace(' ', '')
                    hours = hours.replace('|', ',')
                    if hours != '' and hours != 'ΚΛΕΙΣΤΟ':
                        op_hours += f'{osm_days[i]} {hours}; '
                    else:
                        continue          
            
            data = {
                'ref': row['ΚΩΔ ΠΕΛΑΤ'],
                'name': row['ΠΕΛΑΤΗΣ'],
                'brand': 'Aegean Oil',
                'street': row['ΔΙΕΥΘΥΝΣΗ'],
                'city': row['ΠΟΛΗ'],
                'website': 'https://aegeanoil.com/',
                'phone': phone,
                'opening_hours': op_hours,
                'lat': float(row['Latitude']),
                'lon': float(row['Longitude']),
            }

            yield GeojsonPointItem(**data)