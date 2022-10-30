# _*_ coding: utf-8 _*_


import scrapy
from locations.categories import Code
from locations.items import GeojsonPointItem
import pycountry
from typing import List, Dict


class VisionexpressSpider(scrapy.Spider):
    name: str = 'visionexpress_dac'
    #brand_name: str = 'visionexpress'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.SPECIALTY_STORE]
    spider_countries: List[str] = [pycountry.countries.lookup('in').alpha_3]
    item_attributes: Dict[str, str] = {'brand': 'Vision Express'}
    allowed_domains: List[str] = ['visionexpress.in']

    # start_urls = ["https://vxpim.visionexpress.in/pim/pimresponse.php/?service=storelocator&store=1"]

    def start_requests(self):
        url: str = 'https://vxpim.visionexpress.in/pim/pimresponse.php/?service=storelocator&store=1'

        headers = {
            'lat': '42.66519',
            'lon': '17.1071373'
        }

        yield scrapy.Request(
            url=url,
            method='GET',
            headers=headers,
            callback=self.parse,
        )

    def parse_contacts(self, response):
        '''
        Parse contact information: phone, email, fax, etc.
        '''

        email: List[str] = [
            response.xpath("//*[@id='shops']/div/div/div/footer/div/div/div[6]/div/ul/li[2]/a/text()").get()
        ]

        dataUrl: str = 'https://vxpim.visionexpress.in/pim/pimresponse.php/?service=storelocator&store=1'

        yield scrapy.Request(
            dataUrl,
            callback=self.parse,
            cb_kwargs=dict(email=email)
        )

    def parse(self, response,email: List[str]):
        '''
        @url https://visionexpress.in/findstore
        @returns items 110 150
        @scrapres ref name addr_full city state postcode phone website lat lon opening_hours
        '''

        responseData = response.json()
        for row in responseData['result']:
            data = {
                'ref': row.get('store_id'),
                'name': row.get('name'),
                'addr_full': row.get('address'),
                'city': row.get('city'),
                'state': row.get('state'),
                'postcode': row.get('postcode'),
                'email': email,
                'phone': row.get('store_phone'),
                'website': 'https://visionexpress.in/',
                'lat': float(row.get('lat')),
                'lon': float(row.get('lng')),
                'opening_hours': row.get('store_timing'),
            }
            yield GeojsonPointItem(**data)
