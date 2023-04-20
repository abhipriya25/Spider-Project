# -*- coding: utf-8 -*-

import scrapy
from locations.items import GeojsonPointItem
from bs4 import BeautifulSoup
from locations.categories import Code
import pycountry

class CoffeeIslandSpider(scrapy.Spider):
    
    name = "coffee_island_dac"
    brand_name = "COFFEE ISLAND"
    spider_type = "chain"
    spider_chain_id = 25802
    spider_categories = [Code.SPECIALTY_STORE]
    spider_countries = [pycountry.countries.lookup('gr').alpha_3]
    allowed_domains = ["coffeeisland.gr"]

    start_urls = ["https://coffeeisland.gr/stores/index"]
    
    def parse(self, response):
        '''
        @url https://www.coffeeisland.gr/stores/index
        @returns items 470 480
        @scrapes ref addr_full opening_hours phone website lat lon
        '''

        doc = BeautifulSoup(response.text)
        div = doc.find_all('div', class_='popup-store-link')
        for row in div:
            try:
                website = row.find('div', class_='font-1-1x font-weight-600 mb-2').find('a')['href']
            except:
                website = ''

            p = row.find('div', class_='d-block').find_all('p', class_='mb-2')
            
            # Opening hours
            op = p[1].text.split('takeaway: ')[1]
            if op != '-':
                op = op.replace(' - ', '-').replace(',', ';')
                op = f'Mo-Su {op}'
            else:
                op = ''
            
            try:
                phone = p[2].text
            except:
                pass
            data = {
                'ref': row['data-marker-id'],
                'addr_full': p[0].text,
                'phone': [phone],
                'website': website,
                'opening_hours': op,
                'lon': float(row['data-longitude']),
                'lat': float(row['data-latitude']),
            }

            yield GeojsonPointItem(**data)