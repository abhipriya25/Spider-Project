import scrapy
from locations.items import GeojsonPointItem
from locations.categories import Code
import re
import uuid
import pycountry
from scrapy import Selector

class PuneUrbanCoOpBankDacSpider(scrapy.Spider):
    name = 'pune_urban_co-op_bank_dac'
    brand_name = 'Pune Urban Co-op Bank'
    spider_type = 'chain'
    spider_chain_id = 2640
    spider_chain_name = 'Pune Urban Co-op Bank'
    spider_categories = [Code.BANK, Code.ATM]
    spider_countries = [pycountry.countries.lookup('ind').alpha_3]
    allowed_domains = ['www.puneurbanbank.in']
    start_urls = ['https://www.puneurbanbank.in/Contact.aspx']

    def parse(self, response):
        '''
        @url https://www.puneurbanbank.in/Contact.aspx
        @returns items 15 25
        @scrapes addr_full lat lon
        '''
        for line in response.xpath('//div[contains(@class, "column four")]').getall():
            phone = []
            email = ''
            addr_full = Selector(text=line).xpath('//div[@class="small-icon-text clear-after"]/p[1]/text()').get()
            name = Selector(text=line).xpath('//div[@class="small-icon-text clear-after"]/h4/text()').get()
            coordinates = Selector(text=line).xpath(
                '//div[@class="small-icon-text clear-after"]/table/tr/td/a/@href').get()
            coordinates = re.search('(?<=/@)(.*)(?=,17z)', coordinates).group()
            coordinates = coordinates.split(',')
            for item in Selector(text=line).xpath('//div[@class="small-icon-text clear-after"]/p').getall():
                item_title = Selector(text=item).xpath('//p/b').getall()
                item_title = ''.join(item_title)
                if 'Phone' in item_title:
                    number = ','.join(Selector(text=item).xpath('//p/text()').getall())
                    number = number.replace('/', ',').replace('-', '')
                    number = number.split(',')
                    phone.extend(number)
                if 'Mobile' in item_title:
                    number = ','.join(Selector(text=item).xpath('//p/text()').getall())
                    number = number.replace('/', ',').replace('-', '')
                    number = number.split(',')
                    phone.extend(number)
                if 'Email' in item_title:
                    email = Selector(text=item).xpath('//p/text()').getall()

            store = {
                     'chain_name': self.spider_chain_name,
                     'chain_id': self.spider_chain_id,
                     'brand': self.brand_name,
                     'ref': uuid.uuid4().hex,
                     'name': name,
                     'addr_full': addr_full,
                     'phone': phone,
                     'email': email,
                     'website': 'https://www.puneurbanbank.in/',
                     'lat': coordinates[0],
                     'lon': coordinates[1]
                     }
            yield GeojsonPointItem(**store)
