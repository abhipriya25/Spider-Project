# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict

class AcsSpider(scrapy.Spider):
    name: str = 'acs_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.COURIERS]
    spider_countries: List[str] = [pycountry.countries.lookup('gr').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'ACS'}
    allowed_domains: List[str] = ['acscourier.net']

    def start_requests(self):
        url = 'https://api.acscourier.net/api/locators/branches'
        headers = {
            'accept': 'application/json',
            'origin': 'https://www.acscourier.net',
            'x-encrypted-key': 'CfDJ8K8bqRJwGMpArr9JVm4T1V-i7jn0LnNQUwFKB26aBvy1j3NEfJgWup1TgaY-epWj4ZaLHTnZfsX3cvS76DZGmRN83Hz1KcIbYt9rG0M7DpvhyqCuKM8kj0cyJWfVmq9RCeRPHfV_fzFCeVN5DcH08AkShacXjTLY6uIGtD1NZcl9YY8HUNj1_dHhQJHg8Bw'
        }
        # !!! ATTENTION !!!
        # Noticed that
        # 'x-encrypted-key' changes every ~10min
        # Go to https://www.acscourier.net/el/myacs/ta-ergaleia-mou/anazitisi-simeiwn/
        # On a browser console->network
        # CHeck 'branches' request -> headers -> request headers
        # Get the new value

        yield scrapy.Request(
            url=url,
            headers=headers
        )
    
    def parse(self, response):
        '''
            Returns 717 features (2022-06-01)
            Request link returns a json
        '''
        responseData = response.json()['items']

        typeMatch = {1:"Κεντρικό ", 2:"Περιφερειακό", 3:"Reception",
                4:"Shop in a Shop", 5:"Kiosk", 7:"Smartpoint CPP",
                8:"Smartpoint APP", 9:"Shell Dealers",
                10:"HUB", 11:"Smartpoint Coral"}
    
        for i,row in enumerate(responseData):    
            # Parse opening hours
            try:
                weekdays = row['workingHours'].replace('24ΩΡΟ', '00.00-23.59').replace(' & ', ', ')
            except:
                weekdays = ''
            try:
                sat = row['workingHoursOnSaturday'].replace('24ΩΡΟ', '00.00-23.59').replace(' & ', ', ')
            except:
                sat = ''

            if sat == "ΚΛΕΙΣΤΑ":
                open = f'Mo-Fr {weekdays}'
            else:
                open = f'Mo-Fr {weekdays}; Sa {sat}'

            try:
                phone = row['phones']
            except:
                phone = ''
            try:
                email = row['eMail']
            except:
                email = ''


            # Parse data
            data = {
                'ref': f"{i}_{row['storeDescriptionWithServices']}",
                'brand': 'ASC',
                'name': row['storeDescriptionWithServices'],
                'addr_full': row['storeAddress'],
                'phone': phone,
                'website': 'https://www.acscourier.net/',
                'email': email,
                'opening_hours': open,
                'lat': float(row['latitude']),
                'lon': float(row['longtitude']),
                #'extras': typeMatch[row['typeId']]
            }
            yield GeojsonPointItem(**data)