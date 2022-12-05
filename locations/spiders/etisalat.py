import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict


class EtisalatSpider(scrapy.Spider):
    name: str = 'etisalat_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.TELEPHONE_SERVICE]
    spider_countries: List[str] = [pycountry.countries.lookup('ae').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'Etisalat'}
    allowed_domains: List[str] = ['etisalat.ae']

    def start_requests(self):
        url: str = "https://www.etisalat.ae/content/dam/etisalat/prod-mock-assets/storesnew.json"
        headers = {
            'sdata': 'eyJjaGFubmVsIjoid2ViIiwiYXBwbGljYXRpb25fb3JpZ2luIjoiaW53aS5tYSIsInV1aWQiOiIwMmU1NmNhOS03ZTBjLTQ5YzktYmVjZS1hNGRmZWI5ODEzOWYiLCJsYW5ndWFnZSI6ImZyIiwiYXBwVmVyc2lvbiI6MX0='
        }

        yield scrapy.Request(
            url=url,
            headers=headers,
            callback=self.parse
        )

    def parse(self, response):
        responseData = response.json()

        for row in responseData['data']:
            data = {
                'ref': row['locationId'],
                'name': row['name'],
                'addr_full': row['address1'],
                'city': row['address2'],
                'website': 'https://www.etisalat.ae/',
                'lat': float(row['lat']),
                'lon': float(row['lng']),
            }

            yield GeojsonPointItem(**data)
