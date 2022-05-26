# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict
from bs4 import BeautifulSoup
import re

class JetOilSPider(scrapy.Spider):
    name: str = 'jetoil_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.PETROL_GASOLINE_STATION]
    spider_countries: List[str] = [pycountry.countries.lookup('gr').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'JET Oil'}
    allowed_domains: List[str] = ['jetoil.gr']

    def start_requests(self):
        url = 'https://www.jetoil.gr/el/petrol-stations'
        
        yield scrapy.Request(
            url=url
        )


    def parse(self, response):
        doc = BeautifulSoup(response.text)
        js = doc.find_all('script')[16].text
        js = ' '.join(js.split())

        # google.maps.Marker takes a dictionary as parameter
        # This json has location and title
        pat = re.compile(r'google.maps.Marker\((.*?)\);') # \ cancels the enter ( in string
        shops = pat.findall(js)
        # Now we have a list with all these dictionaries (as strings)

        for i, row in enumerate(shops):
            latPat = re.compile(r'lat: (.*?),')
            lat = latPat.findall(row)[0]
            lngPat = re.compile(r'lng: (.*?)\}')
            lon = lngPat.findall(row)[0]
            titlePat = re.compile(r'title: (.*?) \}')
            title = titlePat.findall(row)[0]
            title = title.replace("'", '')

            data = {
                "ref": int(i),
                "name": title,
                "brand": 'JET Oil',
                "lat": float(lat),
                "lon": float(lon)
            }

            yield GeojsonPointItem(**data)