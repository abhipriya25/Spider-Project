from typing import List, Dict

import pycountry
import scrapy
import json

from locations.categories import Code
from locations.items import GeojsonPointItem


class BlackberysSpider(scrapy.Spider):
    name: str = 'Blackberys_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.CLOTHING_AND_ACCESSORIES]
    spider_countries: List[str] = [pycountry.countries.lookup('in').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'BlackBerrys'}
    allowed_domains: List[str] = ['www.blackberrys.com', 'blackberrys.com']

    def start_requests(self):
        '''
        Spider entrypoint.
        Request chaining starts from here.
        '''
        url: str = "https://storeapi.sekel.tech/v1/stores-cities/4d612d3a-b433-46b5-82c2-0181d72fde05/"

        yield scrapy.Request(
            url=url,
            callback=self.parse_cities
        )

    def parse_cities(self, response):
        responseData = response.json()
        new_responseData = responseData['data']['cities']
        List_cities = []

        for i in new_responseData:
            Str = (i.replace(" ", ""))
            List_cities.append(Str)

        for i in List_cities:
            url: str = "https://storeapi.sekel.tech/v1/store-ivr-list/4d612d3a-b433-46b5-82c2-0181d72fde05/?city=" + i
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                dont_filter=True,
            )
    def parse_opening_hours(self, data) -> str:
        #вложенная функция, видна только внутри функции parse_opening_hours
        def parse_op_hours_of_day(day_full, time_opening, time_closed) -> str:
            try:
                return f'{day_full}: {f"{time_opening} Opening "}-{f" {time_closed} Closing"};'
            except KeyError:
                return f'{day_full}: 00:00-24:00;'

        dictionary = json.loads(data)

        opening_hours: List[str] = [
            parse_op_hours_of_day("Monday", str(dictionary["Monday"])[2:9], str(dictionary["Monday"])[10:-2]),
            parse_op_hours_of_day("Tuesday", str(dictionary["Tuesday"])[2:9], str(dictionary["Tuesday"])[10:-2]),
            parse_op_hours_of_day('Wednesday', str(dictionary["Wednesday"])[2:9], str(dictionary["Wednesday"])[10:-2]),
            parse_op_hours_of_day('Thursday', str(dictionary["Thursday"])[2:9], str(dictionary["Thursday"])[10:-2]),
            parse_op_hours_of_day('Friday', str(dictionary["Friday"])[2:9], str(dictionary["Friday"])[10:-2]),
            parse_op_hours_of_day('Saturday', str(dictionary["Saturday"])[2:9], str(dictionary["Saturday"])[10:-2]),
            parse_op_hours_of_day('Sunday', str(dictionary["Sunday"])[2:9], str(dictionary["Sunday"])[10:-2]),
        ]

        return " ".join(opening_hours)

    def parse(self, response):

        responseData = response.json()

        for row in responseData['data']:
            data = {
                'ref': row['id'],
                'name': row['name'],
                'addr_full': row['address'],
                'city': row['city'],
                'state': row['state'],
                'country': row['country'],
                'email': row['email'],
                'website': 'https://blackberrys.com/',
                'phone': row['number'],
                'opening_hours': self.parse_opening_hours(row['operation_hours']),
                'lat': float(row['latitude']),
                'lon': float(row['longitude']),
            }

            yield GeojsonPointItem(**data)