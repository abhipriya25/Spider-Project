# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem
import requests

class AVSpider(scrapy.Spider):
    name = 'av_dac'
    allowed_domains = ['av.ru/']
    start_urls = ['https://av.ru/ajax/shops/?region=msk&address=']

    def parse(self):
        #response = requests.get("https://av.ru/ajax/shops/?region=msk&address=", headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"})
        #data = response.json()
        data = requests.get("https://av.ru/ajax/shops/?region=msk&address=", headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"}).json()

        for i in range(len(data)):
            item = GeojsonPointItem()

            item['ref'] = data[i]['id']
            item['brand'] = 'Azbuka Vkusa'
            item['addr_full'] = data['address']
            item['country'] = 'Russia'
            item['phone'] = '74955043487|74952230200'
            item['website'] = 'https://av.ru/'
            item['email'] = 'welcome@azbukavkusa.ru'
            item['lat'] = data[i]['coordinates'][0]
            item['lon'] = data[i]['coordinates'][1]

            yield item