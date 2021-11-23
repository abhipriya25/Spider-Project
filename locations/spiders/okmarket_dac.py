# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem
import uuid
import re
import json


class OkmarketSpider(scrapy.Spider):

    name = 'okmarket_dac'
    allowed_domains = ['okmarket.ru']

    def start_requests(self):
        url = 'https://www.okmarket.ru/stores/'
        yield scrapy.Request(
            url=url,
            method='GET',
            callback=self.parse_city,
        )

    def parse_city(self, response):
        data = re.search(r"JSON\.parse\('(.*)'\);", response.text).group(1)
        data_city_id = json.loads(data)['cityList']
        for el in data_city_id:
            yield scrapy.Request(
                url=f'https://www.okmarket.ru/ajax/map_filter/search/?lang=ru&city_id={el["id"]}&type=shop',
                method='GET',
                callback=self.parse,
                cb_kwargs=dict(city=el['name'])
            )

    def parse(self, response, city):
        data = response.json()['data']['shops']
        for row in data:
            item = GeojsonPointItem()

            coords = row['coords']
            item['name'] = row['name']
            item['country'] = 'Россия'
            item['ref'] = row['id']
            item['brand'] = 'О’КЕЙ'
            item['addr_full'] = f'{city}, {row["address"]}'
            item['phone'] = {
                'call_center': '8 (495) 970-00-08',
                'shop': row['phone'][0]['label']
            }
            item['city'] = city
            item['opening_hours'] = f'Без выходных {row["time"]["label"]}'
            item['website'] = 'https://www.okmarket.ru'
            item['lat'] = float(coords['latitude'])
            item['lon'] = float(coords['longitude'])

            yield item
