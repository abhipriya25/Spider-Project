# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem

class KritikosSpider(scrapy.Spider):
    name = 'kritikos_dac'
    allowed_domains = ['kritikos-sm.gr']
    start_urls = ['https://kritikos-sm.gr/_next/data/Q4NMWlOILb4ZX8bHO4nXo/stores.json']

    DAY_REPLACE = {
        'ΔΕΥΤΕΡΑ': 'Mo',
        'ΤPIΤΗ': 'Tu',
        'ΤΕΤAΡΤΗ': 'We',
        'ΠEΜΠΤΗ': 'Th',
        'ΠΑΡΑΣΚΕΥΗ': 'Fr',
        'ΣΑΒΒΑΤΟ': 'Sa',
        'ΚΥΡΙΑΚΗ': 'Su'
    }

    def parse(self, response):
        self.data = response.json()['pageProps']
        
        brand = 'Kritikos'
        country = 'Ελλάδα'
        website = 'https://kritikos-sm.gr/'

        for row in self.data['stores']:
            item = GeojsonPointItem()
            state = self.get_state(row.get('uuid'))

            item['ref'] = row.get('uuid')
            item['name'] = row.get('title')
            item['brand'] = brand
            item['addr_full'] = '{0}, {1}, {2}'.format(country, state, row.get('fields')['address'])
            item['state'] = state
            item['country'] = country
            item['lat'] = row.get('fields')['coordinates'][1]
            item['lon'] = row.get('fields')['coordinates'][0]
            item['website'] = website
            item['phone'] = row.get('phone')
            item['opening_hours'] = self.parse_time(row.get('fields')['work_hours'])

            yield item
    
    def get_state(self, uuid: str) -> str:
        state = ''
        for region in self.data['regions']:
            ids = region['fields']['stores']
            if uuid in ids:
                state = region['title']
        
        return state
    
    def parse_time(self, time: str) -> dict:
        working_hours = {}
        data = time.split('\r\n')

        for row in data:

            print('ROW >>> ', row.split(' ', 1)[0])

            for day in self.DAY_REPLACE:
                days = row.split(' ', 1)[0].replace(day, self.DAY_REPLACE[day])
            
            print('DAYS >>> ', days)

            working_hours[days] = row.split(' ', 1)[1]
        
        return working_hours
