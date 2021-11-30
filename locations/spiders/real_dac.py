# -*- coding: utf-8 -*-
import json

import scrapy
import re
from locations.items import GeojsonPointItem


class RealSpider(scrapy.Spider):
    name = 'real_dac'
    allowed_domains = ['real.hu']
    start_urls = ['https://real.hu/get_markers.php?telepules=&iranyitoszam=&id=']

    def parse(self, response):
        data = response.text
        data = re.findall(r'<markers>([^*]+)</markers>', data)
        data = data[0]
        data = re.split(r'</marker>', data)
        data.pop()
        i = 0
        for row in data:
            splitted_row = row.split('\n')
            splitted_address = splitted_row[5].split('<br />')

            item = GeojsonPointItem()

            item['ref'] = i
            item['brand'] = 'Real'
            item['postcode'] = re.findall(r'\d+', splitted_row[5])[0]
            item['country'] = 'Hungary'
            item['website'] = 'https://real.hu/'
            item['addr_full'] = re.findall(r'\w+', splitted_address[0])[1] + ',' + splitted_address[1]
            item['email'] = 'mail@real.hu'
            item['lat'] = float(re.findall(r'<lat>([^*]+)</lat>', row)[0])
            item['lon'] = float(re.findall(r'<lng>([^*]+)</lng>', row)[0])

            i += 1

            yield item
