# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem
from locations.categories import Code
import re
import pycountry
import uuid

class SuperdryDacSpider(scrapy.Spider):
    name = 'superdry_dac'
    brand_name = 'Superdry'
    spider_type = 'chain'
    spider_chain_name = 'Superdry'
    spider_chain_id = 7583
    spider_categories = [Code.CLOTHING_AND_ACCESSORIES]
    spider_countries = [pycountry.countries.lookup('ind').alpha_3]
    allowed_domains = ['www.superdry.in']
    start_urls = ['https://www.superdry.in/index.php?route=extension/module/wk_store_locater/setter']

    def parse(self, response):
        '''
        @url https://www.superdry.in/index.php?route=extension/module/wk_store_locater/setter
        @returns items 90 100
        @scrapes addr_full lat lon
        '''
        data = response.xpath('/html/body').get()
        data = data.split('!Superdry')
        for item in data:
            if '!none!!' in item:
                lat = ''
                lon = ''
                if '!!http' in item:
                    addr_full = re.search('(.*)(?=!!http)', item).group()
                elif '!!0!' in item:
                    addr_full = re.search('(.*)(?=!!0!)', item).group()
                else:
                    addr_full = re.search('(.*)(?=!!1!)', item).group()
                coordinates = re.search('(?<=!!!!~)(.*)', item).group()
                coordinates = coordinates.split('!')
                if len(coordinates) == 3:
                    lat = coordinates[1]
                    lon = coordinates[2]
                store = {
                    'chain_name': self.spider_chain_name,
                    'chain_id': self.spider_chain_id,
                    'brand': self.brand_name,
                    'ref': uuid.uuid4().hex,
                    'addr_full': addr_full,
                    'lat': lat,
                    'lon': lon,
                    'website': 'https://www.superdry.in/'
                }
                yield GeojsonPointItem(**store)
