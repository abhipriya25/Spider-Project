import scrapy
from locations.items import GeojsonPointItem
import re

class SparSpider(scrapy.Spider):

    name = 'spar_dac'
    allowed_domains = ['spar.ru']
    start_urls = ['https://spar.ru/stores']

    def parse(self, response):
        data = response.css("script")[9].get().replace("\t","").replace("\n","").split("myGeoObject = new ymaps.GeoObject")[1:]

        for row in data:
            item = GeojsonPointItem()
            
            coordinates = re.search(r"coordinates: \[(\d*\.\d*), (\d*\.\d*)\]", row)

            item['ref'] = re.search(r"myGeoObjects\[(\d{,3})\]", row).group(1)
            item['country'] = 'Russia'
            item['brand'] = 'SPAR'
            item['addr_full'] = re.search(r"address: '(.*)',city", row).group(1)
            item['phone'] = "8 (800) 500-13-29"
            item['website'] = 'https://spar.ru'
            item['lat'] = float(coordinates.group(1))
            item['lon'] = float(coordinates.group(2))

            yield item