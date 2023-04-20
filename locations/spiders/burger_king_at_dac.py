import scrapy
from locations.items import GeojsonPointItem
from locations.categories import Code
import pycountry
import uuid
import re
from scrapy import Selector
from bs4 import BeautifulSoup

class BurgerKingAtDacSpider(scrapy.Spider):
    name = 'burger_king_at_dac'
    brand_name = 'BURGER KING'
    spider_type = 'chain'
    spider_chain_id = '1498'
    spider_categories = [Code.FAST_FOOD]
    spider_countries = [pycountry.countries.lookup('at').alpha_3]
    allowed_domains = ['burgerking.at']

    start_urls = [
        'https://www.burgerking.at/getgeopoints?filter=&restrictToCountry=1&country=at']

    def parse(self, response):
        '''
        @url https://www.burgerking.at/getgeopoints?filter=&restrictToCountry=0&country=nl
        '''
        responseData = response.json()
        for item in responseData:
            url = f'https://www.burgerking.at/getstorebubbleinfo?storeId={item["storeId"]}'

            yield scrapy.FormRequest(
                url=url,
                method='GET',
                meta={
                    'lat': item['latitude'],
                    'lon': item['longitude']
                },
                callback=self.parse_store,
            )

    def parse_store(self, response):
        responseData = response.text
        link = re.search(
            '(?<=kingfinder..)(.*)(?=\\\\u0027\\\\u003E\\\\n)', responseData).group()
        base_url = 'https://www.burgerking.at/kingfinder/'
        url = base_url + link
        yield scrapy.FormRequest(
            url=url,
            method='GET',
            meta={'lat': response.meta['lat'],
                  'lon': response.meta['lon'],
                  'store_url': url},
            callback=self.parse_data,
        )

    def hours_generator(self, table_rows):
        hours_mapping = {
            "montag": "Mo",
            "dienstag": "Tu",
            "mittwoch": "We",
            "donnerstag": "Th",
            "freitag": "Fr",
            "samstag": "Sa",
            "sonntag": "Su",
            "gesloten": "off",
        }

        for row in table_rows:
            day, work_hours = row.find_all("td")

            day = day.text.lower()
            day = hours_mapping[day]
            
            work_hours = "off" if work_hours.text == "gesloten" else work_hours.text

            yield f"{day} {work_hours}"

    def parse_hours(self, html) -> str:
        soup = BeautifulSoup(html)

        table_rows = soup.find(
            "table", {"class", "openingtimes"}).find_all("tr")
        opening_hours: str = "; ".join(list(self.hours_generator(table_rows)))

        return opening_hours

    def parse_data(self, response):

        opening_hours: str = self.parse_hours(response.text)
        phone = response.xpath(
            '//*[@id="content"]/div[3]/div[1]/div[1]/table[1]/tr[2]/td[2]/p/text()').get()
        
        phone_list = [phone] if phone is not None else []

        addr_full = response.xpath(
            '//*[@id="content"]/div[3]/div[1]/div[1]/table[1]/tr[1]/td[2]/p/text()').getall()
        addr_full = ' '.join(addr_full)

        store = {
            'ref': uuid.uuid4().hex,
            'chain_name': "BURGER KING",
            'chain_id': "1498",
            'website': 'https://www.burgerking.at/',
            'phone': phone_list,
            'addr_full': addr_full,
            'opening_hours': opening_hours,
            'store_url': response.meta['store_url'],
            'lat': response.meta['lat'],
            'lon': response.meta['lon'],
        }
        yield GeojsonPointItem(**store)
