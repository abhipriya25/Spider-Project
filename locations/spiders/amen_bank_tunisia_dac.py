import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List
from bs4 import BeautifulSoup, Comment
import uuid
import re

class AmenBankTunisia(scrapy.Spider):
    name = 'amen_bank_tunisia_dac'
    brand_name = "Amen Bank Tunisia"
    spider_type: str = 'chain'
    spider_chain_name = 'Amen Bank Tunisia'
    spider_chain_id = 23103
    spider_categories: List[str] = [Code.BANK]
    spider_countries: List[str] = [pycountry.countries.lookup('tn').alpha_2]
    allowed_domains: List[str] = ['www.amenbank.com.tn']
    start_urls = ['https://www.amenbank.com.tn/fr/reseau-agences.html']

    def start_requests(self):
        '''
        Spider entrypoint. 
        Request chaining starts from here.
        '''
        url: str = "https://www.amenbank.com.tn/fr/reseau-agences.html"


        yield scrapy.FormRequest(
            url=url,
            method='GET',
            callback = self.parse_cities
        )

    def parse_cities(self, response):
        '''
        Getting the names of all the cities
        Request chaining to extract data for each city
        '''
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        conteiner = soup.find("form", {"id": "SearchAgencyForm"}).find_all("option")
        for row in conteiner[1:]:
            form_data = {'gov': f'{row.text}'}
            yield scrapy.FormRequest(
                url="https://www.amenbank.com.tn/php/search.php",
                formdata = form_data,
                method='POST',
                callback = self.parse 
            )

    def parse_coordinates(self, row):
        '''
        Extract coordinates from links in comments
        '''
        comment_with_link = row.find(string=lambda text: isinstance(text, Comment))
        pattern = re.compile(r"\d{1,2}\.\d+,\d{1,2}\.\d+")
        matches = re.findall(pattern, comment_with_link)
        lat = matches[0].split(",")[0]
        lon = matches[0].split(",")[1]

        return lat, lon


    def parse(self, response):
        '''
        Extract data for each city
        '''

        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        conteiner = soup.find("div", {"class": "row justify-content-start"})
        data = conteiner.find_all("div", {"class": "box_item bg-white mb-3"})

        for row in data:
            info = row.find_all("p", {"class": "mb-0"})
            lat, lon = self.parse_coordinates(row)
            data = {
                'chain_name': self.spider_chain_name,
                'chain_id': self.spider_chain_id,
                'brand': self.brand_name,
                'ref': uuid.uuid4().hex,
                'name': row.find("h6", {"class": "text-uppercase"}).text,
                'addr_full': info[0].text,
                'city': info[1].text,
                'website': "https://www.amenbank.com.tn/",
                'email': info[3].text,
                'phone': (info[2].text).replace(" ", ""),
                'lat': lat,
                'lon': lon
            }

            yield GeojsonPointItem(**data)
            