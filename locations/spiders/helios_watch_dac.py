# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem
from locations.categories import Code
import pycountry
import uuid

class HeliosWatchDacSpider(scrapy.Spider):
    name = 'helios_watch_dac'
    brand_name = 'Helios Watch'
    spider_type = 'chain'
    spider_chain_name = 'Helios Watch'
    spider_chain_id = 33821
    spider_categories = [Code.SPECIALTY_STORE]
    spider_countries = [pycountry.countries.lookup('ind').alpha_3]
    allowed_domains = ['www.helioswatchstore.com']
    start_urls = ['https://www.helioswatchstore.com/store-locator/storelist']

    def parse_store(self, response):

        name = response.xpath('//*[@id="maincontent"]/div[2]/div/div[6]/div/div/div[3]/h2/text()').get()
        addr_full = ''
        phone = response.xpath('//*[@id="maincontent"]/div[2]/div/div[6]/div/div/div[3]/h4[2]/a/text()').get()
        email = response.xpath('//*[@id="maincontent"]/div[2]/div/div[6]/div/div/div[3]/h4[1]/a/text()').get()
        for item in response.xpath(
                '//*[@id="maincontent"]/div[2]/div/div[6]/div/div/div[3]/div[@class="store_address"]/text()').getall():
            addr_full += item
        store = {

                 'chain_name': self.spider_chain_name,
                 'chain_id': self.spider_chain_id,
                 'brand': self.brand_name,
                 'ref': uuid.uuid4().hex,
                 'name': name,
                 'addr_full': addr_full,
                 'website': 'https://www.helioswatchstore.com/',
                 'phone': phone,
                 'email': email,
                 'store_url': response.meta['start_url']}

        yield GeojsonPointItem(**store)

    def parse_city(self, response):
        for item in response.xpath('//*[@id="loader-example"]/div[2]/div[2]/div/div/@href').getall():
            url = item
            yield scrapy.Request(url, meta={'start_url': url}, callback=self.parse_store)

    def parse_state(self, response):
        for item in response.xpath('//*[@id="city"]/option/@value').getall()[1:]:
            url = "https://www.helioswatchstore.com/store-locator/" + response.meta['item'] + "/" + item
            yield scrapy.Request(url, meta={'start_url': url}, callback=self.parse_city)

    def parse(self, response):
        '''
        @url https://www.helioswatchstore.com/store-locator/storelist
        '''
        for item in response.xpath('//*[@id="state"]/option/@value').getall()[1:]:
            url = 'https://www.helioswatchstore.com/store-locator/' + item
            yield scrapy.Request(url, meta={'start_url': url, 'item': item}, callback=self.parse_state)


