import scrapy
from locations.items import GeojsonPointItem
from locations.categories import Code
import pycountry
import uuid
from scrapy import Selector


class SplashDacSpider(scrapy.Spider):
    name = 'splash_dac'
    brand_name = 'Splash'
    spider_type = 'chain'
    spider_chain_id = 1559
    spider_chain_name = 'Splash'
    spider_categories = [Code.CLOTHING_AND_ACCESSORIES]
    spider_countries = [pycountry.countries.lookup('ind').alpha_3]
    allowed_domains = ['www2.splashfashions.com']

    def start_requests(self):
        url = 'https://www2.splashfashions.com/in/store_callback/Select%20a%20City%2C%20India/javascript_request/null'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76"
        }

        yield scrapy.Request(
            url=url,
            method='GET',
            headers=headers,
            callback=self.parse,
        )

    def parse(self, response):
        '''
        @url https://www2.splashfashions.com/in/store_callback/Select%20a%20City%2C%20India/javascript_request/null
        @returns items 15 22
        @scrapes addr_full lat lon
        '''
        for item in response.xpath('//marker').getall():
            name = Selector(text=item).xpath("//marker/@name").get()
            times = Selector(text=item).xpath("//marker/@timings").get()
            times = times.split('to')
            opening = f'Mo-Su {times[0].replace(" ", "")}-{times[1].replace(" ", "")}'
            phone = Selector(text=item).xpath("//marker/@phone").get()
            phone = phone.replace('-', '')
            phone_list = [phone]
            addr_full = Selector(text=item).xpath("//marker/@address").get()
            lat = Selector(text=item).xpath("//marker/@lat").get()
            lon = Selector(text=item).xpath("//marker/@lng").get()
            store = {
                     'chain_name': self.spider_chain_name,
                     'chain_id': self.spider_chain_id,
                     'brand': self.brand_name,
                     'ref': uuid.uuid4().hex,
                     'website': 'https://www2.splashfashions.com/',
                     'name': name,
                     'opening_hours': opening,
                     'phone': phone_list,
                     'addr_full': addr_full,
                     'lat': lat,
                     'lon': lon
                     }
            yield GeojsonPointItem(**store)
