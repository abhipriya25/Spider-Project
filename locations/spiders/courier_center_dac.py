# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict
import re

class CourierCenterSpider(scrapy.Spider):
    name: str = 'courier_center_dac'
    spider_type: str = 'chain'
    spider_categories: List[str] = [Code.COURIERS]
    spider_countries: List[str] = [pycountry.countries.lookup('gr').alpha_2]
    item_attributes: Dict[str, str] = {'brand': 'Courier Center'}
    allowed_domains: List[str] = ['www.courier.gr']

    def start_requests(self):
        url = 'https://www.courier.gr/physical/stores/markers/s/keq3ke43t6i0fml2jfh948q2l6'
        headers = {
            'cookie': '_ga=GA1.2.937987529.1653915050; frontend=keq3ke43t6i0fml2jfh948q2l6; frontend_cid=hKwylDNjv9bmQRzV; _gid=GA1.2.1944312492.1654165203; _gat_gtag_UA_1370150_52=1'
        }

        yield scrapy.Request(
            url=url,
            headers=headers
        )
    
    def parse(self, response):
        '''
            Returns 107 features (2022-06-01)
        '''
        response = response.text

        # Response is xml
        # Each store is within <marker *data* />
        # The format is...
        # marker_label="6" id="901" name="CC &#x397;&#x3A1;&#x391;&#x39A;&#x39B;&#x395;&#x399;&#x39F; &#x39A;&#x3A1;&#x397;&#x3A4;&#x397;&#x3A3; 2" address="&#x39C;&#x391;&#x39D;&#x39F;&#x3A5; &#x39A;&#x391;&#x3A4;&#x3A1;&#x391;&#x39A;&#x397; 129, 71500, &#x397;&#x3A1;&#x391;&#x39A;&#x39B;&#x395;&#x399;&#x39F; &#x39A;&#x3A1;&#x397;&#x3A4;&#x397;&#x3A3;" phone="2810261479" lat="35.31972" lng="25.11349"
        # !!! NEED TO FIX ENCODING !!!
        markersPat = re.compile('<marker (.*?)/>')
        markers = markersPat.findall(response)

        idPat = re.compile('id="(.*?)"')
        namePat = re.compile('name="(.*?)"')
        addrPat = re.compile('address="(.*?)"')
        phonePat = re.compile('phone="(.*?)"')
        latPat = re.compile('lat="(.*?)"')
        lonPat = re.compile('lng="(.*?)"')

        for marker in markers:
            id = idPat.findall(marker)[0]
            name = namePat.findall(marker)[0]
            addr = addrPat.findall(marker)[0]
            phone = phonePat.findall(marker)[0]
            lat = latPat.findall(marker)[0]
            lon = lonPat.findall(marker)[0]

            data = {
                'ref': id,
                'brand': 'Courier Center',
                'name': name,
                'addr_full': addr,
                'phone': phone,
                'lat': lat,
                'lon': lon
            }
            
            yield GeojsonPointItem(**data)