# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem
import string


class CoopSpider(scrapy.Spider):

    name = 'coop_dac'
    allowed_domains = ['coop.hu']

    def start_requests(self):
        url = 'https://www.coop.hu/wp-admin/admin-ajax.php'
        for symbol in  string.printable: #string.ascii_uppercase + string.digits:
            yield scrapy.FormRequest(
                url=url,
                method='POST',
                formdata={
                    'action': 'getShops',
                    'searchFilters': f'cim={symbol}'
                },
                dont_filter=True,
                callback=self.parse,
            )

    def parse(self, response):
        try:
            data = response.json()['results']
            for row in data:
                item = GeojsonPointItem()

                item['name'] = row['title']
                item['country'] = 'Hungary'
                item['ref'] = row['id']
                item['brand'] = 'COOP'
                item['addr_full'] = f'{row["zip"]} {row["city"]}, {row["address"]}'
                item['phone'] = '+36 (1) 455-5400'
                item['city'] = row["city"]
                item['website'] = f'https://www.coop.hu/uzlet/{row["id"]}'
                item['lat'] = float(row['lat'])
                item['lon'] = float(row['lng'])

                yield item
        except BaseException:
            with open('log', 'a') as f:
                f.write(response.text + '\n')
            return
