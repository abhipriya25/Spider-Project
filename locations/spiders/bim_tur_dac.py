# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict
from bs4 import BeautifulSoup
import uuid

class Bim_TUR_Spider(scrapy.Spider):

    name = "bim_tur_dac"
    brand_name = "Bim"
    spider_type: str = "chain"
    spider_chain_id = 961
    spider_chain_name = "Bim"
    spider_categories: List[str] = [Code.GROCERY]
    spider_countries: List[str] = [pycountry.countries.lookup('tr').alpha_2]
    allowed_domains: List[str] = ['www.bim.com.tr']

    def start_requests(self):
        st_url = "https://www.bim.com.tr/Categories/104/magazalar.aspx"

        yield scrapy.Request(
            url=st_url,
            method='GET',
            callback=self.get_cities,
        )

    def get_cities(self,response):

        soup = BeautifulSoup(response.text, 'lxml')
        select = soup.find('select',{"id":"BimFiltre_DrpCity"})
        select = select.findAll('option')

        for k in select:
            
            link = "https://www.bim.com.tr/Categories/104/magazalar.aspx?CityKey="+k['value']

            yield scrapy.Request(
                url=link,
                method='GET',
                dont_filter=True,
                callback=self.get_counties,
            )
            

    def get_counties(self, response):

        soup = BeautifulSoup(response.text, 'lxml')
        select = soup.find('select',{"id":"BimFiltre_DrpCounty"})
        select = select.findAll('option')
        
        for k in select:

            link = response.url+"&CountyKey="+k['value']+"&firin=0"

            yield scrapy.Request(
                url=link,
                method='GET',
                dont_filter=True,
                callback=self.parse,
            )

    def parse(self, response):

        soup = BeautifulSoup(response.text, 'lxml')
        select = soup.findAll('div',{"class": "box"})

        for k in select:

            data = {
                'ref': uuid.uuid4().hex,
                'chain_name': self.spider_chain_name,
                'chain_id': self.spider_chain_id,
                'brand': self.brand_name,
                'name': k.find("h3").contents[0],
                'addr_full': k.find("p").contents[0],
                'country': self.spider_countries,
                'website': 'https://www.bim.com.tr',
                'store_url': response.url
            }

            yield GeojsonPointItem(**data)