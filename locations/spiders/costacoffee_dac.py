import scrapy
from locations.categories import Code
from locations.items import GeojsonPointItem
import pycountry
from typing import List, Dict


class CostaCoffeeSpider(scrapy.Spider):
    name = 'costacofee_dac'
    brand_name = 'Costa Coffee'
    spider_type = 'chain'
    spider_categories: List[str] = [Code.BAKERY_AND_BAKED_GOODS_STORE]
    spider_countries: List[str] = [pycountry.countries.lookup('in').alpha_3]
    allowed_domains: List[str] = ['costacoffee.in/']

    start_urls = ["https://www.costacoffee.in/api/cf/?locale=en-IN&include=2&content_type=storeLocatorStore&limit=500&f\
    ields.location[near]=28.553532369889,77.12456293893058"]

    def parse(self, response):

        responseData = response.json()

        for row in responseData['items']:
            data = {
                'ref': row.get(['fields']['storeType']['sys']['id']),
                'name': row.get(['fields']['storeName']),
                'addr_full': row.get(['fields']['storeAddress']),
                'website': 'costacoffee.in/',
                'lat': float(row.get(['fields']['location']['lat'])),
                'lon': float(row.get(['fields']['location']['lon'])),
            }
            yield GeojsonPointItem(**data)
# for item in b:
#     print(item['fields']['storeName'])
#     print(item['fields']['storeAddress'])
#     print(item['fields']['location']['lat'])
#     print(item['fields']['location']['lon'])

