import scrapy
from locations.items import GeojsonPointItem
from locations.categories import Code
import pycountry
import uuid


class BurgerKingFinDacSpider(scrapy.Spider):
    name = 'burger_king_fi_dac'
    brand_name = 'BURGER KING'
    spider_type = 'chain'
    spider_chain_id = "1498"
    spider_categories = [Code.FAST_FOOD]
    spider_countries = [pycountry.countries.lookup('fi').alpha_3]
    allowed_domains = ['burgerking.fi']

    start_urls = ['https://burgerking.fi/wp-json/v2/restaurants']

    def parse(self, response):
        '''
            @url https://burgerking.fi/wp-json/v2/restaurants
            @returns items 50 80
            @scrapes lat lon ref
        '''
        response_data = response.json()

        for item in response_data:
            opening = f'Mo {item["visiting_hours"]["monday"]}; Tu {item["visiting_hours"]["tuesday"]}; We {item["visiting_hours"]["wednesday"]}; ' \
                      f'Th {item["visiting_hours"]["thursday"]}; Fr {item["visiting_hours"]["friday"]}; Sa {item["visiting_hours"]["saturday"]}; ' \
                      f'Su {item["visiting_hours"]["sunday"]}'

            store = {
                'ref': uuid.uuid4().hex,
                'chain_name': "BURGER KING",
                'chain_id': "1498",
                'website': 'https://burgerking.fi',
                'street': item['address'],
                'city': item['city'],
                'name': item['name'],
                'phone': [item['phone']],
                'postcode': item['zip_code'],
                'opening_hours': opening,
                'lat': item['location']['lat'],
                'lon': item['location']['lng']
            }
            yield GeojsonPointItem(**store)
