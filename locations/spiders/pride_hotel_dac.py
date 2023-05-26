# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem
from locations.categories import Code
import pycountry
import re
from scrapy import Selector
import uuid

class PrideHotelDacSpider(scrapy.Spider):
    name = 'pride_hotel_dac'
    brand_name = 'Pride Hotel'
    spider_type = 'chain'
    spider_chain_name = 'Pride Hotel'
    spider_chain_id = 28191
    spider_categories = [Code.HOTEL]
    spider_countries = [pycountry.countries.lookup('ind').alpha_3]
    allowed_domains = ['www.pridehotel.com']
    start_urls = ['https://www.pridehotel.com/contact-us/hotel-directory.html']

    def parse(self, response):
        '''
            @url https://www.pridehotel.com/contact-us/hotel-directory.html
            @returns items 20 25
            @scrapes addr_full ref
        '''
        data = response.xpath('//*[@id="wrapper"]/div/div[2]/div/div/div[1]/div/div/div').getall()
        for item in data:
            addr_full = ''
            phone = ''
            email = ''
            name = ''
            if Selector(text=item).xpath("//div/div/a/text()").getall() is not None:
                for line in Selector(text=item).xpath("//div/div/a/text()").getall():
                    if 'Pride' in line:
                        name = line
                    elif '@' in line:
                        email = line
            for line in Selector(text=item).xpath("//div/div/text()").getall():
                addr_full += line
            if re.search('(?<=Phone:)(.*)', addr_full) is not None:
                phone = re.search('(?<=Phone:)(.*)', addr_full).group()
                phone = re.findall('[0-9]+', phone)
                phone = ''.join(phone)
            if phone == '' and Selector(text=item).xpath('//div/div[3]/span/text()').get() is not None:
                phone = Selector(text=item).xpath('//div/div[3]/span/text()').get()
                phone = re.findall('[0-9]+', phone)
                phone = ''.join(phone)
            if re.search('(.*)(?=\|)', addr_full) is not None:
                addr_full = re.search('(.*)(?=\|)', addr_full).group()
            if name == '' and Selector(text=item).xpath('//div/p[3]/a[1]/text()').get() is not None:
                if Selector(text=item).xpath("//div/p[3]/a/text()").getall() is not None:
                    for line in Selector(text=item).xpath("//div/p[3]/a/text()").getall():
                        if 'Pride' in line:
                            name = line
                        elif '@' in line:
                            email = line
                for line in Selector(text=item).xpath("//div/p[3]/text()").getall():
                    addr_full += line
                if re.search('(?<=Phone:)(.*)', addr_full) is not None:
                    phone = re.search('(?<=Phone:)(.*)', addr_full).group()
                    phone = re.findall('[0-9]+', phone)
                    phone = ''.join(phone)
                if re.search('(.*)(?=\|)', addr_full) is not None:
                    addr_full = re.search('(.*)(?=\|)', addr_full).group()
            if name != '':
                store = {
                         'chain_name': self.spider_chain_name,
                         'chain_id': self.spider_chain_id,
                         'brand': self.brand_name,
                         'ref': uuid.uuid4().hex,
                         'website': 'https://www.pridehotel.com/',
                         'name': name,
                         'addr_full': addr_full,
                         'phone': phone,
                         'email': email}
                yield GeojsonPointItem(**store)
