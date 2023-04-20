import scrapy
from locations.items import GeojsonPointItem
from locations.categories import Code
import pycountry
import uuid


class BurgerKingDKSpider(scrapy.Spider):
    name = 'burger_king_dk_dac'
    brand_name = 'BURGER KING'
    spider_type = 'chain'
    spider_chain_id = "1498"
    spider_categories = [Code.FAST_FOOD]
    spider_countries = [pycountry.countries.lookup('dk').alpha_3]
    allowed_domains = [
        'www.burgerking.dk',
        'bk-dk-ordering-api.azurewebsites.net'
    ]

    # start_urls = ['https://www.burgerking.dk']

    def start_requests(self):
        url = 'https://bk-dk-ordering-api.azurewebsites.net/api/v2/restaurants?latitude=55.6774425609295&longitude=12.56875951826194&radius=99900000&top=500'

        yield scrapy.Request(
            url,
            method="GET",
            callback=self.parse
        )

    def parse(self, response):
        '''
            @url https://bk-dk-ordering-api.azurewebsites.net/api/v2/restaurants?latitude=55.6774425609295&longitude=12.56875951826194&radius=99900000&top=500
            @returns items 50 80
            @scrapes lat lon ref
        '''
        response_data = response.json()
        for item in response_data['data']:
            store = {
                'ref': uuid.uuid4().hex,
                'chain_name': "BURGER KING",
                'chain_id': "1498",
                'name': item['storeName'],
                'addr_full': item['storeAddress'].replace("\t", ","),
                'website': 'https://www.burgerking.dk/',
                'lat': item['storeLocation']['coordinates']['latitude'],
                'lon': item['storeLocation']['coordinates']['longitude']
            }
            yield GeojsonPointItem(**store)
