import scrapy
from locations.items import GeojsonPointItem
import json
import re

class MariaRaSpider(scrapy.Spider):

    name = 'maria_ra_dac'
    allowed_domains = ['maria-ra.ru']
    start_urls = ['https://www.maria-ra.ru/o-kompanii/karta-seti/']


    def parse(self, response):
        data_script = response.css("script")[16].get()
        json_data = re.findall(r"(?<=let \$objects = JSON.parse\(').*(?='\);)", data_script)
        data = json.loads(json_data[0])
        i = 0
        for row in data:
            item = GeojsonPointItem()

            coordinates = row["COORDINATE"].split(",")

            item['ref'] = i
            item['country'] = "Russia"
            item['brand'] = 'Maria Ra'
            item['addr_full'] = row["NAME"]
            item['phone'] = '8-800-1000-810'
            item['website'] = 'https://www.maria-ra.ru/'
            item['email'] = 'ura@maria-ra.ru'
            item['opening_hours'] = f'everyday: {row["STARTED_WORK"]}-{row["END_WORK"]}'
            item['lat'] = float(coordinates[0])
            item['lon'] = float(coordinates[1])
            i += 1
            yield item