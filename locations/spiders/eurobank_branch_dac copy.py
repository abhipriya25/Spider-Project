# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem
from locations.categories import Code
import pycountry

class EurobankBranchSpider(scrapy.Spider):
    name = 'eurobank_branch_dac'
    brand_name = "Eurobank"
    spider_type = "chain"
    spider_chain_id = "2335"
    spider_categories = [Code.ATM]
    spider_countries = [pycountry.countries.lookup('gr').alpha_3]
    allowed_domains = ["eurobank.gr"]

    start_urls = ['https://www.eurobank.gr/en/api/branch/get?type=branch&vendor=']

    def parse(self, response):
        '''
        @url https://www.eurobank.gr/en/api/branch/get?type=branch&vendor=
        @returns items 270 280
        @scrapes ref name addr_full phone website lat lon
        '''
        data = response.json()

        for row in data['results']:
            data = {
                "ref": row['branchId'],
                "chain_id": "2335",
                "chain_name": "Eurobank",
                "name": row['name'],
                'addr_full': row['ds']['address'],
                'phone': [row['ds']['tel']],
                'website': 'https://www.eurobank.gr/',
                'email': [row['ds']['emailUrl']],
                'lat': float(row['lc']['lat']),
                'lon': float(row['lc']['lng']),
            }

            yield GeojsonPointItem(**data)