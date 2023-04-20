# -*- coding: utf-8 -*-

import scrapy
from locations.items import GeojsonPointItem
import uuid
from locations.categories import Code
import pycountry

class EkoSpider(scrapy.Spider):
    name = 'eko_cyp_dac'
    brand_name = "EKO"
    spider_type = "chain"
    spider_chain_id = 1007
    spider_categories = [Code.PETROL_GASOLINE_STATION]
    spider_countries = [pycountry.countries.lookup('cyp').alpha_3]
    allowed_domains = ["eko.com.cy"]

    start_urls = ["https://www.eko.com.cy/en/stations/katastimata/"]

    def parse(self, response):
        '''
        @url https://www.eko.com.cy/en/stations/katastimata/
        @returns items 90 100
        @scrapes ref name addr_full phone website email lat lon
        '''
        data = response.css('div[class*="box-info"]')
        
        for row in data:
            item = GeojsonPointItem()

            name = row.css('div div[class*="name-container"] span *::text').get()
            city_street_housenumber = row.css('li[class*="address-one"] *::text').get()
            phone = [row.css('li[class*="phone"] *::text').get()]

            item['ref'] = uuid.uuid4().hex
            item['name'] = name
            item['chain_name'] = "EKO"
            item['chain_id'] = "1007"
            item['addr_full'] = city_street_housenumber
            item['phone'] = phone
            item['website'] = "https://www.eko.com.cy"
            item['lat'] = float(row.attrib['data-latitude'])
            item['lon'] = float(row.attrib['data-longitude'])

            yield item
