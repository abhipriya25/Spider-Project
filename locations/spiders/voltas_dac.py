# -*- coding: utf-8 -*-
import json
import re
import uuid
import requests
import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict

class VoltasSpider(scrapy.Spider):
    name = 'voltas_dac'
    brand_name = 'Voltas'
    spider_type: str = 'chain'
    spider_chain_name = 'Voltas'
    spider_chain_id = 34420
    spider_categories: List[str] = [Code.CONSUMER_ELECTRONICS_STORE]
    spider_countries: List[str] = [pycountry.countries.lookup('in').alpha_2]
    allowed_domains: List[str] = ['www.myvoltas.com']

    def start_requests(self):

        url: str = 'https://www.myvoltas.com/storelocator/dealerData.php'

        i = 0
        while i < 33:
            i += 1
            yield scrapy.FormRequest(
                url=url,
                method= "POST",
                formdata={"state": str(i)},
                callback=self.second_requests
            )

    def second_requests(self, response):

        surl: str = "https://www.myvoltas.com/storelocator/getstore.php"

        values = response.xpath('//option/@value').getall()

        for elem in values:

            yield scrapy.FormRequest(
                url=surl,
                method= "POST",
                formdata={"city": str(elem)},
                callback=self.parse
            ) 

    def parse(self, response):
        item = GeojsonPointItem()
        data = response

        if data != None:

            stores: dict = data.json()
            for store in stores:
                item['ref'] = uuid.uuid1().hex
                item['name'] = store['StoreName']
                item['addr_full'] = store['StoreAddress1']
                if store['StorePhone'] != "":
                    item['phone'] = re.split(",|/", store['StorePhone'])
                item['city'] = store['CityName']
                item['website'] = "https://www.myvoltas.com"
                item['email'] = "vcare@voltas.com"
                if store['lat'] != "":
                    item['lat'] = store['lat']
                    item['lon'] = store['longt']

                item['chain_name'] = self.spider_chain_name
                item['chain_id'] = self.spider_chain_id
                item['brand'] = self.brand_name

                yield item
