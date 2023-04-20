import scrapy
from locations.items import GeojsonPointItem
from locations.categories import Code
import pycountry
import uuid


class BurgerKingSESpider(scrapy.Spider):
    name = 'burger_king_se_dac'
    brand_name = 'BURGER KING'
    spider_type = 'chain'
    spider_chain_id = '1498'
    spider_categories = [Code.FAST_FOOD]
    spider_countries = [pycountry.countries.lookup('se').alpha_3]
    allowed_domains = [
        'burgerking.se',
        'bk-se-ordering-api.azurewebsites.net'
    ]

    # start_urls = ['https://burgerking.se/']

    def start_requests(self):
        url = 'https://bk-se-ordering-api.azurewebsites.net/api/v2/restaurants?latitude=59.330311012767446&longitude=18.068330468145753&radius=99900000&top=500'

        yield scrapy.Request(
            url,
            method="GET",
            callback=self.parse
        )

    def parse(self, response):
        '''
        @url https://bk-se-ordering-api.azurewebsites.net/api/v2/restaurants?latitude=59.330311012767446&longitude=18.068330468145753&radius=99900000&top=500
        @returns items 100 140
        @scrapes lat lon
        '''
        response_data = response.json()

        for item in response_data['data']:
            store = {
                'ref': uuid.uuid4().hex,
                'name': item['storeName'],
                'addr_full': item['storeAddress'].replace("\t", ","),
                'chain_name': "BURGER KING",
                'chain_id': "1498",
                'website': 'https://burgerking.se',
                'lat': item['storeLocation']['coordinates']['latitude'],
                'lon': item['storeLocation']['coordinates']['longitude']
            }
            yield GeojsonPointItem(**store)
