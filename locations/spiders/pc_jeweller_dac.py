# -*- coding: utf-8 -*-
import scrapy
import re
import uuid
from locations.items import GeojsonPointItem
from locations.categories import Code
from scrapy import Selector
from typing import List, Dict
import pycountry

class PcJewellerDacSpider(scrapy.Spider):
    name = 'pc_jeweller_dac'
    brand_name = 'PC Jeweller'
    spider_type = 'chain'
    spider_chain_name = 'PC Jeweller'
    spider_chain_id = 34246
    spider_categories = [Code.FLOWERS_AND_JEWELRY]
    spider_countries = [pycountry.countries.lookup('ind').alpha_3]
    allowed_domains = ['corporate.pcjeweller.com']
    start_urls = ['https://corporate.pcjeweller.com/store-locator/']

    def parse(self, response):

        elems = response.xpath('//div[contains(@class, "accordion-content")]//li').getall()

        print(elems)

        for item in elems:

            name = Selector(text=item).xpath('//h4/text()').get()

            if name:

                raw_s = Selector(text=item).xpath('//p/text()').getall()
                
                addr_full = ''
                city = ''
                street = ''
                postcode = ''
                phone = ''

                street = raw_s[0] 

                if not raw_s[1].replace('\n','').isdigit(): 
                    city = raw_s[1]
                    addr_full = city + ', ' + street
                    postcode = raw_s[2]
                    phone = raw_s[3]
                else:
                    addr_full = street
                    postcode = raw_s[1]
                    phone = raw_s[2]

                phone = phone.split(',')

                for s in range(len(phone)):
                    phone[s] = re.sub(r'\D', '', phone[s])

                store = {
                    'chain_name': self.spider_chain_name,
                    'chain_id': self.spider_chain_id,
                    'brand': self.brand_name,
                    'ref': uuid.uuid4().hex,
                    'name': name.replace('\n',''),
                    'addr_full': addr_full.replace('\n',''),
                    'website': 'https://corporate.pcjeweller.com/',
                    'postcode': postcode.replace('\n',''),
                    'phone': phone
                }
                yield GeojsonPointItem(**store)
