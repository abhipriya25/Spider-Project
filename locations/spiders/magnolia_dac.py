# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem
from bs4 import BeautifulSoup as bfs
import re
import requests
import json
import pandas as pd
class MagnoliaSpider(scrapy.Spider):
    name = 'magnolia_dac'
    allowed_domains = ['shop.mgnl.ru']
    start_urls = ['https://shop.mgnl.ru/contacts/stores/']

    def parse(self, response):
        data = self.data_preparation().to_json()
        i = 0
        for row in data:
            item = GeojsonPointItem()
            item['ref'] = i
            item['brand'] = 'Magnolia'
            item['country'] = 'Russia'
            item['addr_full'] = row['addr']
            item['website'] = 'https://shop.mgnl.ru/contacts/stores/'
            item['lat'] = row['lat']
            item['lon'] = row['lon']
            i+=1
            yield item

    def data_preparation(self):
        base_url = requests.get("https://shop.mgnl.ru/contacts/stores/").text
        soup = bfs(base_url)
        correct_result= [script for script in soup.find_all('script') if "var shop" in script.text]
        text_result = correct_result[0].text
        pop_result_addr = re.findall('"addr".*', text_result)
        pop_result_coord = re.findall('"coord.*', text_result)
        for i in range(len(pop_result_addr)):
            pop_result_addr[i] = pop_result_addr[i].replace('"addr":"', '')
            pop_result_addr[i] = pop_result_addr[i].replace('"', '')
            pop_result_coord[i] = pop_result_coord[i].replace('"coord":"', '')
            pop_result_coord[i] = pop_result_coord[i].replace('"', '')
        lat = []
        lon = []
        for i in range(len(pop_result_coord)):
            dubl = pop_result_coord[i]
            lat.append(float(pop_result_coord[i][:dubl.find(",")-1]))
            lon.append(float(pop_result_coord[i][dubl.find(",")+1:-1]))
        data = pd.DataFrame(pop_result_addr,columns={'addr'})
        data['lat'] = lat
        data['lon'] = lon
        return data
