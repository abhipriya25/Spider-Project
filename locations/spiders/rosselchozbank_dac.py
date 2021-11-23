# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem


class RosselchozbankSpider(scrapy.Spider):

    name = 'rosselchozbank_dac'
    allowed_domains = ['rshb.ru']

    def start_requests(self):
        url = 'https://www.rshb.ru/offices/rostov/'
        yield scrapy.Request(
            url=url,
            method='GET',
            dont_filter=True,
            callback=self.parse_city
        )

    def parse_city(self, response):
        data = response.css(
            "span[class*='b-branches-item-link js-branches-item']::attr(data-branch-code)")
        for branchCode in data:
            yield scrapy.FormRequest(
                url=f'https://www.rshb.ru/ajax/get-data.php',
                method='POST',
                formdata={'branchCode': branchCode.get(),
                          'type': 'offices.list'},
                dont_filter=True,
                callback=self.parse_office
            )
            yield scrapy.FormRequest(
                url=f'https://www.rshb.ru/ajax/get-data.php',
                method='POST',
                formdata={'branchCode': branchCode.get(),
                          'type': 'atms.list'},
                dont_filter=True,
                callback=self.parse_atm
            )

    def parse_atm(self, response):
        data = response.json()['atmItems']
        for id in list(data):
            data_point = data[id]
            item = GeojsonPointItem()

            item['name'] = f'Банкомат - {data_point["name"]}'
            item['country'] = 'Russia'
            item['ref'] = id
            item['brand'] = 'РоссельхозБанк'
            item['addr_full'] = data_point['address']
            item['phone'] = '8 (800) 100-0-100'
            item['opening_hours'] = 'круглосуточно'
            item['website'] = 'https://www.rshb.ru/'
            item['lat'] = float(data_point['location_lat'])
            item['lon'] = float(data_point['location_lng'])

            yield item

    def parse_office(self, response):
        data = response.json()['officeItems']
        for id in list(data):
            data_point = data[id]
            item = GeojsonPointItem()

            item['name'] = data_point["name"]
            item['country'] = 'Russia'
            item['ref'] = id
            item['brand'] = 'РоссельхозБанк'
            item['addr_full'] = data_point['address']
            item['phone'] = '8 (800) 100-0-100'
            item['opening_hours'] = {'individual': data_point['individual_mode'],
                                     'legalEntity': data_point['company_mode']}
            item['website'] = 'https://www.rshb.ru/'
            item['lat'] = float(data_point['location_lat'])
            item['lon'] = float(data_point['location_lng'])

            yield item
