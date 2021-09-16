# -*- coding utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem


class SovcombankSpider(scrapy.Spider):
    name = 'sovcombank_dac'
    allowed_domains = ['sovcombank.ru']
    status_url = ['https://prod-api.sovcombank.ru/points?lang=ru&location=55.641533109991876,37.42227915722656,55.86612820665731,37.82190684277345&type=office&reference=55.753993,37.622093&for_individual=true']

    def parse(self, response):
        data = response.json()

        for row in data:
            item = GeojsonPointItem()

            street = row.get('street_address')
            city = row.get('region')
            country = 'Russia'
            postcode = row.get('postal_code')

            item['ref'] = row['id']
            item['brand'] = 'Sovcombank'
            item['addr_full'] = f'{postcode},{country},{city},{street}'
            item['street'] = street
            item['city'] = city
            item['postcode'] = postcode
            item['country'] = country
            item['website'] = 'https://www.bricomarche.pl/'
            item['phone'] = '78001000006|74959880000'
            item['website'] = 'https://sovcombank.ru/'
            item['lat'] = float(row['location'][0])
            item['lon'] = float(row['location'][1])



            yield item