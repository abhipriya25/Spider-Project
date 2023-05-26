# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem
from locations.categories import Code
import pycountry
import re
from scrapy import Selector
import uuid

class SangliCoopBankDacSpider(scrapy.Spider):
    name = 'sangli_coop_bank_dac'
    brand_name = 'Sangli Co-op Bank'
    spider_type = 'chain'
    spider_chain_name = 'Sangli Co-op Bank'
    spider_chain_id = 2637
    spider_categories = [Code.BANK, Code.ATM]
    spider_countries = [pycountry.countries.lookup('ind').alpha_3]
    allowed_domains = ['www.sangliurbanbank.in']
    start_urls = ['https://www.sangliurbanbank.in/branch_locator.html']

    def parse(self, response):
        '''
        @url https://www.sangliurbanbank.in/branch_locator.html
        @returns items 30 40
        @scrapes addr_full phone
        '''
        for line in Selector(text=response.text).xpath('//*[@id="option12"]/div').getall():
            addr_full = ''
            phone_code = ''
            phone_list = []
            name = Selector(text=line).xpath('//div/div/text()').get()
            name = str(name).replace(':', '')
            for item in Selector(text=line).xpath('//div/text()').getall():
                addr_full += str(item)

            if re.search('(?<=Ph:)(.*)', addr_full):

                phone = re.search('(?<=Ph:)(.*)', addr_full).group()
                if '(' in phone:
                    phone_code = re.search('(?<=\()(.*)(?=\))', phone).group()
                elif '-' in phone:
                    phone_code = re.search('(.*)(?=-)', phone).group()
                phone = phone.replace(phone_code, '').replace('(', '').replace(')', '').replace('-', '')
                
            addr_full = re.search('(.*)(?=Ph:)', addr_full).group()
            addr_full = addr_full.strip()
            phone = phone.split(',')
            for number in phone:
                phone_list.append(phone_code + number)

            store = {
                'chain_name': self.spider_chain_name,
                'chain_id': self.spider_chain_id,
                'brand': self.brand_name,
                'ref': uuid.uuid4().hex,
                'name': name,
                'addr_full': addr_full,
                'phone': phone_list,
                'website': 'https://www.sangliurbanbank.in/'
            }

            yield GeojsonPointItem(**store)
