 # -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict
from bs4 import BeautifulSoup
import uuid
import re

class Neopolitan_Pizza_IND_Spider(scrapy.Spider):

    name = "neopolitan_pizza_ind_dac"
    brand_name = "Neopolitan Pizza"
    spider_type: str = "chain"
    spider_chain_id = 28318
    spider_chain_name = "Neopolitan Pizza"
    spider_categories: List[str] = [Code.RESTAURANT]
    spider_countries: List[str] = [pycountry.countries.lookup('in').alpha_2]
    allowed_domains: List[str] = ['www.neopolitanpizza.in']

    def start_requests(self):

        st_url = "https://www.neopolitanpizza.in/location.php"

        yield scrapy.Request(
            url=st_url,
            method='GET',
            callback=self.parse,
        )

        sec_url = "https://www.neopolitanpizza.in/franchise/location_api/listing_record"

        headers = {
            "accept": "*/*",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "sec-ch-ua": "\"Chromium\";v=\"112\", \"Google Chrome\";v=\"112\", \"Not:A-Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-requested-with": "XMLHttpRequest",
            "cookie": "ci_session=fcb9bd7b046de5e1a161ab31e3fc84e04c1e12df",
            "Referer": "https://www.neopolitanpizza.in/location.php",
            "Referrer-Policy": "strict-origin-when-cross-origin"
        }

        raw_body = 'token=P0uepqSfNgV6j&s=&param%5Bper_page%5D=20&param%5Bpage%5D=0&param%5BTotal%5D=&param%5Bbind_id%5D=%23result'

        yield scrapy.Request(
            url=sec_url,
            headers=headers,
            body=raw_body,
            method='POST',
            callback=self.parse,
        )

    def parse(self, response):

        try:
            soup = BeautifulSoup(response.json()['html'], 'lxml')
        except:
            soup = BeautifulSoup(response.text, 'lxml')

        select = soup.findAll('div',{"class": 'address'})

        for k in select:

            b = k.findAll('li')

            address = ''
            mobile = ''
            email = ''

            for j in range(len(b)):
                if j == 0:
                    address = b[j].text.replace("\t", "").replace("\n", "")
                if j == 1:
                    mobile = '+' + str(re.sub("[^0-9]", "", b[j].text))
                if j == 2:
                    if b[j].find('a'):
                        if b[j].find('a')['href'].find('mailto') != -1:
                            email = b[j].find('a').text

            data = {
                'ref': uuid.uuid4().hex,
                'chain_name': self.spider_chain_name,
                'chain_id': self.spider_chain_id,
                'brand': self.brand_name,
                'addr_full': address,
                'phone': mobile,
                'email': email,
                'country': self.spider_countries,
                'website': 'https://www.neopolitanpizza.in'
            }

            yield GeojsonPointItem(**data)