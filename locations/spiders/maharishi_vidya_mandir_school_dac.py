import scrapy
from locations.categories import Code
from locations.items import GeojsonPointItem
import pycountry
from scrapy import Selector
import uuid
import re


class MaharishiVidyaMandirSchoolDacSpider(scrapy.Spider):
    name = 'maharishi_vidya_mandir_school_dac'
    brand_name = 'Maharishi Vidya Mandir School'
    spider_type = 'chain'
    spider_chain_id = 34074
    spider_chain_name = 'Maharishi Vidya Mandir School'
    spider_categories = [Code.SCHOOL]
    spider_countries = [pycountry.countries.lookup('ind').alpha_3]
    #allowed_domains = ['www.maharishividyamandir.com']
    start_urls = ['https://www.maharishividyamandir.com/mvm-branches']

    def parse_school_1(self, response):
        name = Selector(text=response.text).xpath('//*[@id="info"]/text()').get()
        addr_full = ''
        mphone = ''
        phone = ''
        email = ''
        phone_list = []
        item_holder = ''
        data = Selector(text=response.text).xpath('//*[@class="border_me"][1]').get()
        for item in Selector(text=data).xpath('//div/ul/li[1]/div/text()').getall():
            addr_full += item
        addr_full = addr_full.replace('\n', '').replace('\r', '').replace('\xa0', '').replace(':', '')
        addr_full = ' '.join(addr_full.split())
        addr_full = addr_full.strip()
        for item in Selector(text=data).xpath('//div/ul/text()').getall():
            mphone += item
            mphone = ' '.join(mphone.split())

        text = Selector(text=data).xpath('//div/ul/li[2]/b/text()').get()
        for item in Selector(text=data).xpath('//div/ul/li[2]/text()').getall():
            phone += item
        if '@' in phone:
            email = phone
            phone = ''
        elif 'Fax' in text:
            phone = ''
        phone = phone.replace('-', '').replace(' ', '')
        if mphone != '':
            mphone = mphone.replace('\n', '')
            mphone = mphone.split('/')
            phone_list += mphone
        if phone != '':
            phone = phone.replace('\n', '')
            phone = phone.split('/')
            phone_list += phone

        for item in Selector(text=data).xpath('//div/ul/li[3]/text()').getall():
            item_holder += item
        if '@' in item_holder:
            email += item_holder

        item_holder = ''
        for item in Selector(text=data).xpath('//div/ul/li[4]/text()').getall():
            item_holder += item
        if '@' in item_holder:
            email += item_holder

        store = {
                 'chain_name': self.spider_chain_name,
                 'chain_id': self.spider_chain_id,
                 'brand': self.brand_name,
                 'ref': uuid.uuid4().hex,
                 'name': name,
                 'addr_full': addr_full,
                 'website': 'https://www.maharishividyamandir.com/',
                 #'store_url': response.meta['store_url'],
                 'phone': phone_list,
                 'email': email
                 }
        yield GeojsonPointItem(**store)

    def parse_school(self, response):
        addr_full = ''
        email = ''
        phone = ''
        if Selector(text=response.text).xpath('//*[@id="main-nav"]/ul/li[8]/a/@href').get() is not None:
            link = Selector(text=response.text).xpath('//*[@id="main-nav"]/ul/li[8]/a/@href').get()
            if 'http' in link:
                url = link
            else:
                if '/' in link:
                    url = response.meta['start_url'] + link
                else:
                    url = response.meta['start_url'] + '/' + link
            yield scrapy.Request(url, meta={'start_url': url, 'store_url': response.meta['start_url']},
                                 callback=self.parse_school_1)
        elif Selector(text=response.text).xpath('//*[@id="navbar-collapse"]/ul/li[8]/a/@href').get() is not None:
            link = Selector(text=response.text).xpath('//*[@id="navbar-collapse"]/ul/li[8]/a/@href').get()
            base = response.meta['start_url']
            base = base.replace('.org/', '.org')
            if '/' in link:
                url = base + link
            else:
                url = base + '/' + link
            yield scrapy.Request(url, meta={'start_url': url, 'store_url': response.meta['start_url']},
                                 callback=self.parse_school_1)
        elif Selector(text=response.text).xpath('//*[@id="navbarSupportedContent"]/ul/li[8]/a/@href').get() is not None:
            link = Selector(text=response.text).xpath('//*[@id="navbarSupportedContent"]/ul/li[8]/a/@href').get()
            url = link
            yield scrapy.Request(url, meta={'start_url': url, 'store_url': response.meta['start_url']},
                                 callback=self.parse_school_1)
        elif Selector(text=response.text).xpath(
                '//*[@id="main"]/div[4]/div/div[2]/div[3]/div/p[1]/span/b/text()').get() is not None:
            name = Selector(text=response.text).xpath(
                '//*[@id="main"]/div[4]/div/div[2]/div[3]/div/p[1]/span/b/text()').get()
            for item in Selector(text=response.text).xpath(
                    '//*[@id="main"]/div[4]/div/div[2]/div[3]/div/p[2]/text()').getall():
                addr_full += item
            addr_full = addr_full.replace('\n', '').replace('\r', '').replace('\xa0', '').replace(':', '')
            addr_full = ' '.join(addr_full.split())
            addr_full = addr_full.strip()
            if Selector(text=response.text).xpath(
                    '//*[@id="main"]/div[4]/div/div[2]/div[3]/div/p[3]').get() is not None:
                phone = Selector(text=response.text).xpath(
                    '//*[@id="main"]/div[4]/div/div[2]/div[3]/div/p[3]').get()
                phone = re.sub('<.*?>', '', phone)
                phone = phone.replace(' ', '').replace(':', '').replace('-', '').replace('\n', '')
                phone = phone.split('/')
            if Selector(text=response.text).xpath(
                    '//*[@id="main"]/div[4]/div/div[2]/div[3]/div/p[4]').get() is not None:
                mphone = Selector(text=response.text).xpath(
                    '//*[@id="main"]/div[4]/div/div[2]/div[3]/div/p[4]').get()
                if '@' in mphone:
                    email = Selector(text=response.text).xpath(
                        '//*[@id="main"]/div[4]/div/div[2]/div[3]/div/p[4]/a/text()').get()
                else:
                    mphone = Selector(text=response.text).xpath(
                        '//*[@id="main"]/div[4]/div/div[2]/div[3]/div/p[4]/text()').get()
                    mphone = mphone.replace(' ', '').replace(':', '').replace('\n', '')
                    phone.append(mphone)
            if Selector(text=response.text).xpath(
                    '//*[@id="main"]/div[4]/div/div[2]/div[3]/div/p[5]/a/text()').get() is not None:
                email = Selector(text=response.text).xpath(
                    '//*[@id="main"]/div[4]/div/div[2]/div[3]/div/p[5]/a/text()').get()

            store = {
                     'chain_name': self.spider_chain_name,
                     'chain_id': self.spider_chain_id,
                     'brand': self.brand_name,
                     'ref': uuid.uuid4().hex,
                     'name': name,
                     'addr_full': addr_full,
                     'website': 'https://www.maharishividyamandir.com/',
                     #'store_url': response.meta['start_url'],
                     'email': email,
                     'phone': phone
                   }
            yield GeojsonPointItem(**store)

    def parse(self, response):
        '''
            @url https://www.maharishividyamandir.com/mvm-branches
        '''
        for item in response.xpath('/html/body/div[4]/div[2]/div[1]/div[2]/div[5]/table/tr/td[4]/a/@href').getall():
            url = item
            yield scrapy.Request(url, meta={'start_url': url}, callback=self.parse_school)

