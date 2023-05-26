# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict
from bs4 import BeautifulSoup
import uuid
import re

class Donde_Comer_Galicia_ESP_Spider(scrapy.Spider):

    name = "donde_comer_galicia_esp_dac"
    brand_name = "Dónde comer Galicia"
    spider_type: str = "generic"
    spider_chain_id = 0
    spider_chain_name = "Dónde comer Galicia"
    spider_categories: List[str] = [Code.HOTEL]
    spider_countries: List[str] = [pycountry.countries.lookup('es').alpha_2]
    allowed_domains: List[str] = ['www.turismo.gal']

    def start_requests(self):
        st_url = "https://www.turismo.gal/localizador-de-recursos/-/sit/donde_comer/galicia?langId=es_ES&items=100&indexPage=1"       

        yield scrapy.Request(
            url=st_url,
            cookies={
                'GUEST_LANGUAGE_ID':'en_US',
                'TGWS_ID': 'prd-weblogic-c03-0011.xunta.local'
            },
            method='GET',
            callback=self.get_page,
        )

    def get_page(self, response):

        soup = BeautifulSoup(response.text, 'lxml')
        
        #self.get_data(response)

        item_count = soup.find('li', {'class':'pagination-input'}).text
        item_count = re.sub("[^0-9]", "", item_count)

        for i in range(1,int(item_count)+1):

            link = "https://www.turismo.gal/localizador-de-recursos/-/sit/donde_comer/galicia?langId=es_ES&items=100&indexPage=" + str(i)

            yield scrapy.Request(
                url=link,
                method='GET',
                callback=self.get_data,
            )
        
    def get_data(self, response):

        soup = BeautifulSoup(response.text, 'lxml')
        all_links = soup.findAll('a', {'class':'title mod-href'})

        for k in all_links:

            link = 'https://www.turismo.gal/'+ k['href'] + '&p_p_state=exclusive'

            yield scrapy.Request(
                url=link,
                method='GET',
                meta={'dont_merge_cookies': True},
                callback=self.parse,
            )

    # def coordinates(self, row):
    #     coord_mass = row.find('strong').text.replace('\t',' ').split('-')

    #     pattern = r"[-]?\d+(?:.\d+)?"

    #     lat =  re.findall(pattern, coord_mass[0])
    #     lon =  re.findall(pattern, coord_mass[1])

    #     lat = float(lat[0]) + float(lat[1])/60 + float(lat[2])/3600
    #     lon = -(float(lon[0]) + float(lon[1])/60 + float(lon[2])/3600)
        
    #     return [lat,lon]
    
    def parse(self, response):

        soup = BeautifulSoup(response.text, 'lxml')
        
        if soup:

            name = ''
            lat = ''
            lon = ''
            postcode = ''
            region = ''
            street = ''
            housenumber = ''
            telephone = ''

            name = soup.findAll('meta', {'itemprop':'name'})
            lat = soup.find('meta', {'itemprop':'latitude'})
            lon = soup.find('meta', {'itemprop':'longitude'})
            postcode = soup.find('meta', {'itemprop':'postalCode'})
            region = soup.find('meta', {'itemprop':'addressRegion'})
            street = soup.find('meta', {'itemprop':'addressLocality'})
            housenumber = soup.find('meta', {'itemprop':'streetAddress'})
            telephone = soup.find('meta', {'itemprop':'telephone'})

            if name:
                name = name[1]['content'].replace('\t','').replace('  ','')

            if lat:
                lat = lat['content'].replace('\t','').replace('  ','')

            if lon:
                lon = lon['content'].replace('\t','').replace('  ','')

            if postcode:
                postcode = postcode['content'].replace('\t','').replace('  ','')

            if telephone:
                telephone = telephone['content'].replace('\t','').replace('  ','')

            if street:
                street = street['content'].replace('\t','').replace('  ','')

            if housenumber: 
                housenumber = housenumber['content'].replace('\t','').replace('  ','')

            if region:
                region = region['content'].replace('\t','').replace('  ','')

            addr_full = f'{street}, {housenumber}, {region}, {postcode}'

            if name:

                data = {
                    'ref': uuid.uuid4().hex,
                    'chain_name': self.spider_chain_name,
                    'chain_id': self.spider_chain_id,
                    'brand': self.brand_name,
                    'name': name,
                    'addr_full': addr_full,
                    'phone': telephone,
                    'housenumber': housenumber,
                    'street': street,
                    'postcode': postcode,
                    'country': self.spider_countries,
                    'store_url': response.url.replace('&p_p_state=exclusive',''), 
                    'website': "https://www.turismo.gal",
                    'lat': lat,
                    'lon': lon,
                }

                yield GeojsonPointItem(**data)

