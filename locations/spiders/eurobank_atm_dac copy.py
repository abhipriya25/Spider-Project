# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem
from locations.categories import Code
import pycountry

class EurobankAtmSpider(scrapy.Spider):
    
    name = "eurobank_atm_dac"
    brand_name = "Eurobank"
    spider_type = "chain"
    spider_chain_id = "2335"
    spider_categories = [Code.ATM]
    spider_countries = [pycountry.countries.lookup('gr').alpha_3]
    allowed_domains = ["eurobank.gr"]
    
    # start_urls = ['https://www.eurobank.gr/en/api/branch/get?type=atm&vendor=']

    def start_requests(self):
        yield scrapy.Request(
            url='https://www.eurobank.gr/en/contact-phone-numbers',
            method='get',
            callback=self.parse_contact
        )

    def parse_contact(self, response):
        phone = [
            response.xpath(
                "/html/body/div[1]/header/div/div/nav[1]/div/div[2]/ul/li[2]/a/text()").get()
        ]
        email = [
            response.xpath(
                '/html/body/div[1]/section[2]/div/div/div[2]/div/div[1]/div/article/div[2]/div[1]/div[2]/a/text()').get()
        ]

        yield scrapy.Request(
            url='https://www.eurobank.gr/en/api/branch/get?type=atm&vendor=',
            method='GET',
            callback=self.parse,
            cb_kwargs=dict(phone=phone, email=email)
        )

    def parse(self, response, phone, email):
        '''
        @url https://www.eurobank.gr/en/api/branch/get?type=atm&vendor=
        @returns items 980 1000
        @scrapes ref name addr_full phone website lat lon
        '''
        data = response.json()

        for row in data['results']:
            data = {
                "ref": row['id'],
                "chain_id": "2335",
                "chain_name": "Eurobank",
                'addr_full': row['ds']['address'],
                'phone': phone,
                'opening_hours': row['ds']['hourstatusTxt'],
                'website': 'https://www.eurobank.gr/',
                'email': email,
                'lat': float(row['lc']['lat']),
                'lon': float(row['lc']['lng']),
            }

            yield GeojsonPointItem(**data)