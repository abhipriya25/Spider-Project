# -*- coding: utf-8 -*-

import scrapy
from locations.items import GeojsonPointItem
import uuid
from locations.categories import Code
import pycountry

class EkoSpider(scrapy.Spider):
    name = 'eko_mne_dac'
    brand_name = "EKO"
    spider_type = "chain"
    spider_chain_id = 1007
    spider_categories = [Code.PETROL_GASOLINE_STATION]
    spider_countries = [pycountry.countries.lookup('mne').alpha_3]
    allowed_domains = ["jugopetrol.co.me"]

    start_urls = ["https://www.jugopetrol.co.me/en/stations/find-station/"]

    def parse(self, response):
        '''
        @url https://www.jugopetrol.co.me/en/stations/find-station/
        @returns items 40 60
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
            item['website'] = "https://www.jugopetrol.co.me"
            item['lat'] = float(row.attrib['data-latitude'])
            item['lon'] = float(row.attrib['data-longitude'])

            yield item
