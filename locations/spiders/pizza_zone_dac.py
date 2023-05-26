# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem
from locations.categories import Code
import pycountry
import uuid
from scrapy import Selector
import re

class PizzaZoneDacSpider(scrapy.Spider):
    name = 'pizza_zone_dac'
    brand_name = 'Pizza Zone'
    spider_type = 'chain'
    spider_chain_name = 'Pizza Zone'
    spider_chain_id = 34191
    spider_categories = [Code.RESTAURANT]
    spider_countries = [pycountry.countries.lookup('in').alpha_3]
    allowed_domains = ['www.pizzazone.co.in']
    start_urls = ['http://www.pizzazone.co.in/restaurant-locator/']

    def parse(self, response):
        '''
        @url http://www.pizzazone.co.in/restaurant-locator/
        @returns items 20 27
        @scrapes addr_full lat lon
        '''
        for s in response.xpath('/html/body/div[2]/section[2]/div/div/div').getall():

            for item in Selector(text=s).xpath('//section/div/div').getall():

                addr_full = ''
                addr = ''
                phone_list = []
                lat = ''
                lon = ''
                name = Selector(text=item).xpath('//div/div/div/h3/text()').get()
                if Selector(text=item).xpath('//div/div/div/h3/span/text()').get() is not None:
                    name += Selector(text=item).xpath('//div/div/div/h3/span/text()').get()
                if Selector(text=item).xpath('//div/div/div/p/span/text()').get() is not None:
                    addr_full += Selector(text=item).xpath('//div/div/div/p/span/text()').get()
                for thing in Selector(text=item).xpath('//div/div/div/p/text()').getall():
                    addr_full += thing
                if 'Ph.' in addr_full:
                    phone = re.search('(?<=Ph\.)(.*)', addr_full).group()
                    addr_full = addr_full.replace(phone, '').replace('Ph.', '').replace('\n', '')
                    phone = phone.replace(':', '').replace('-', '').replace(' ', '').replace('\t','')
                    phone_list.append(phone)
                elif 'M.' in addr_full:
                    phone = re.search('(?<=M\.)(.*)', addr_full).group()
                    addr_full = addr_full.replace(phone, '').replace('M.', '').replace('\n', '')
                    phone = phone.replace(':', '').replace('-', '').replace(' ', '').replace('\t','')
                    phone_list.append(phone)
                if Selector(text=item).xpath('//div/div[2]/a/@href') is not None:
                    lat_lon = Selector(text=item).xpath('//div/div[2]/a/@href').get()
                    if lat_lon is not None:
                        lat_lon = re.search('(?<=@)(.*)(?=z/data)', str(lat_lon)).group()
                        lat_lon = lat_lon.split(',')
                        lat = lat_lon[0]
                        lon = lat_lon[1]

                store = {
                    'chain_name': self.spider_chain_name,
                    'chain_id': self.spider_chain_id,
                    'brand': self.brand_name,
                    'name': name.replace('\t','').replace('\n', ''),
                    'addr_full': addr_full.replace('\t','').replace('\n', '').replace("\xa0", ''),
                    'phone': phone_list,
                    'ref': uuid.uuid4().hex,
                    'website': 'http://www.pizzazone.co.in/',
                    'lat': lat,
                    'lon': lon
                }
                yield GeojsonPointItem(**store)
