# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem
import uuid


class PochtaBankSpider(scrapy.Spider):

    name = 'pochtabank_dac'
    allowed_domains = ['pochtabank.ru']
    start_urls = ['https://my.pochtabank.ru/api/mapsdkpoi/map?&type=postEmployeeInPostOffice&type=clientCenter&type=miniOffice&type=bankEmployeeInPostOffice&type=terminal&type=mfc&type=atmPochtaBank&type=atmVTB&tile=[0,0]&zoom=0']

    def parse(self, response):
        data = response.json()["data"]["features"]
        for row in data:
            item = GeojsonPointItem()
            type_points = {
                "postEmployeeInPostOffice": "Услуги Банка на Почте России",
                "clientCenter": "Отделение Банка",
                "mfc": "Отделение Банка в МФЦ",
                "terminal": "Окно Почты России с возможностью снятия наличных с банковских карт и внесения наличных на карты Почта Банка",
                "miniOffice": "Мини офис Банка в ТРЦ",
                "bankEmployeeInPostOffice": "Отделение Банка на Почте России",
                "atmPochtaBank": "Банкомат Почта Банк",
                "atmVTB": "Банкомат ВТБ"
            }
            coordinates = row['properties']['location']
            item['name'] = type_points[row['properties']['type']]
            item['ref'] = row['properties']['id']
            item['brand'] = 'Pochta Bank'
            item['country'] = 'Russia'
            item['addr_full'] = row['properties']['address'] if ('address' in row['properties'].keys()) else ""
            item['phone'] = '+7 495 532 13 00'
            item['website'] = 'https://www.pochtabank.ru/'
            item['email'] = 'welcome@pochtabank.ru'
            item['lat'] = float(coordinates['lat'])
            item['lon'] = float(coordinates['lng'])
            yield item
