# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict
import json
import re

class Kfc_saSpider(scrapy.Spider):
    
    name = 'kfc_sa_dac'
    brand_name = 'KFC'
    spider_type = 'chain'
    spider_chain_id = 1559
    spider_chain_name = 'KFC'
    spider_categories: List[str] = [Code.FAST_FOOD]
    spider_countries: List[str] = [pycountry.countries.lookup('sa').alpha_2]
    allowed_domains: List[str] = ['saudi.kfc.me']
    
    def start_requests(self):
        
        url = "https://saudi.kfc.me/api/getStoreList" 
        
        headers = {
            "Content-Type": "application/json"
        }

        payload = {"payload":{"path":"https://AmfProdNeStorage.azureedge.net/amfprodneblobstorage/production/","country":"ksa","subPath":"?sv=2019-02-02&ss=bfqt&srt=sco&sp=rl&se=2029-04-09T19:07:24Z&st=2020-04-09T11:07:24Z&spr=https&sig=Z67UuDjY4QScWJCAMeXZmMn7VLH%2F3uL6xv6vpXnInOA%3D"}}
    
        yield scrapy.Request(
            url=url,
            headers=headers,
            method="POST",
            body=json.dumps(payload),
            callback=self.parse
        )
    
    def parse_hours(self,store):
        start_time = store.get('startTime').split('T')[1][:5]
        end_time = store.get('endTime').split('T')[1][:5]

        return f"Mo-Su {start_time}-{end_time}"

    def parse(self,response):
        responseData = response.json()

        for city in responseData:

            for store in city.get('store'):
                
                data = {    
                    'ref': store.get('id'),
                    'chain_name': self.spider_chain_name,
                    'chain_id': self.spider_chain_id,
                    'brand': self.brand_name,
                    'name': city.get('cityName'),
                    'addr_full': store.get('address_en'),
                    'website': 'https://saudi.kfc.me',
                    'phone': store.get('phone1'),
                    'opening_hours': self.parse_hours(store),
                    'store_url': 'https://saudi.kfc.me/en/store/' + re.sub(r"[^a-zA-Z]+", '', store.get('name_en')) + '/' + str(store.get('storeId')),
                    'lat': float(store.get('location').get('latitude', '')),
                    'lon': float(store.get('location').get('longitude', '')),
                }

                yield GeojsonPointItem(**data)