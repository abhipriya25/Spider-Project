# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem
from bs4 import BeautifulSoup
import re
import requests
import json

class MagnumSpider(scrapy.Spider):
    name = 'magnum_dac'
    allowed_domains = ['magnum.kz']

    def start_requests(self):
        url = 'https://magnum.kz/page/magaziny'
        soup = BeautifulSoup(requests.get(url).text,'lxml')
        data_cities = soup.find_all('a', class_ = 'dropdown-item select-city')
        
        for city in data_cities:
            data_city = city.get('data-city')
            json_city = json.loads(data_city)
            cityName = json_city['name'].encode('utf-8')
            cityId = json_city['id']
            payload=f'_token=ZwNqdaYVNcjPNzofelv3rIQJq5IxDXGnzscOjJH7&city_name={cityName}&city_alias={cityName}&city_id={cityId}'
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Cookie': 'XSRF-TOKEN=eyJpdiI6IlgzbW0yK0NFcWNOWEFxUmhNWFJ1K2c9PSIsInZhbHVlIjoiTHFOUDVNcitCNWRPd3NXajNZN05zU3cvb3d2TkNxRGpLanU0QmtZQlVRKzZyWHhUSWRLVTV0ekpNTmhvRGorVmE2SzlxTmtIRHdReDM1S1B3QXAwdUNHZ0VOZ2RwYmpUbkltMjk5UklGVnhEYmQ3OVlyZEtYbWpQVDhDMU9kU0ciLCJtYWMiOiIzODA1NjU2NDM4YjU1ODg2MDhlZjgzOTRhYjlmM2I1ODc4Y2QzMTI5NTc0YTM2YjJlOWViZjVjYzRkYmY0YzIzIn0%3D; magnum_kz_session=eyJpdiI6ImlobFBYOVFEa2tMQi9wR1RraUUzMkE9PSIsInZhbHVlIjoiTlN2d3UveXhIeldCcjE2UnRzcEZ0ZlprbGtJQ0FNaWFmOEEwdkwxcEVyMmxYbEdKTE1xcnlDMVA0Z2o3N3UvTzlnaGpWME8zZU9WWXpRL0RoSVpNclFPdmNBZVBwcURCOGJ4NGg3TjZvMHdWN2ZjR25hNzlhd0pna1NiWGFBdEQiLCJtYWMiOiI3ZjU0ZjdkZjYzZDUyMGIwMWFjMjQ4ZWUwZTQwMGZhZTk3Yzg0Yzg4NjI3MzNjZjkwNjUyNzY3OTNhZjI5OTk1In0%3D'
                }
            # response = requests.request("POST", url, headers=headers, data=payload)
            yield scrapy.Request(
                url=url, 
                method='GET', 
                headers=headers,
                data=payload,
                callback=self.parse,
            )



    def parse(self, response):
        soup = BeautifulSoup(response.text,'lxml')
        data = soup.find_all('li', class_ = 'list-group-item d-flex align-items-center pointer')
        # pipenv run scrapy crawl magnum_dac --output=magnum.geojson
        for row in data:
            item = GeojsonPointItem()
            name_shop = re.findall(r'.*\)', row.text.strip())[0]
            address = re.split(r'.*\)', row.text.strip())[1].strip()
            coords = re.findall(r'(\w*\.\w+)', row.get('data-cords'))

            item['ref'] = row.get('id')
            item['opening_hours'] = row.get('data-mod')
            item['name'] = name_shop
            item['brand'] = 'Magnum'
            item['addr_full'] = address
            item['country'] = 'Kazakhstan'
            item['phone'] = row.get('data-phone')
            item['website'] = 'https://magnum.kz/'
            item['email'] = 'info@magnum.kz'
            item['lat'] = float(coords[0])
            item['lon'] = float(coords[1])

            print(row.get('id'))
            yield item