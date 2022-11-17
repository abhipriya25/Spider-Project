import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict


class AvoskaSpider(scrapy.Spider):
    name: str = 'inwi_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.TELEPHONE_SERVICE]
    spider_countries: List[str] = [pycountry.countries.lookup('ma').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'inwi'}
    allowed_domains: List[str] = ['inwi.ma']

    def start_requests(self):
        url: str = "https://api.inwi.ma/api/v1/ms-content/agencies?ville=&quartier="

        yield scrapy.Request(
            url=url,
            callback=self.parse
        )

    def parse(self, response):
        responseData = response.json()

        for row in responseData:
            data = {
                'ref': row['agencies_id'],
                'addr_full': row['adresse'],
                'city': row.get('quartier'),
                'neighborhood': row.get('ville'),
                'website': 'https://inwi.ma/',
                'lat': float(row['latitude']),
                'lon': float(row['longitude']),
            }

            yield GeojsonPointItem(**data)



