# -*- coding: utf-8 -*-
import scrapy
import re
import json
from locations.items import GeojsonPointItem
from locations.operations import extract_phone, extract_email

class BlinkSpider(scrapy.Spider):

    name = 'blink_dac'
    allowed_domains = ['https://blinkcharging.gr']
    start_urls = ['https://blinkcharging.gr/en/ev-driver/%CF%83%CF%84%CE%B1%CE%B8%CE%BC%CE%BF%CE%AF-%CF%86%CE%BF%CF%81%CF%84%CE%B9%CF%83%CE%B7%CF%82-blink/']

    def parse(self, response):
        sc_selector = response.selector.xpath("//script[@type='text/javascript']")
        script_raw = sc_selector[45].get()
        points_list = re.findall('var marker_object =.+;', script_raw)

        email = response.selector.xpath("//div[@class='footer-cont-ctm']/a[3]/text()").get()
        phone = response.selector.xpath("//div[@class='footer-cont-ctm']/a[2]/text()").get()

        for i in points_list:
            item = GeojsonPointItem()
            json_obj = json.loads(i.replace('var marker_object = cspm_new_pin_object(map_id, ', '').replace(');', ''))
            item['ref'] = json_obj['post_id']
            item['brand'] = 'Blink'
            item['country'] = 'Greece'
            item['addr_full'] = f"{item['country']}, {json_obj['coordinates']['address']}"
            item['phone'] = phone
            item['website'] = json_obj['media']['link']
            item['email'] = email
            item['lat'] = json_obj['coordinates']['lat']
            item['lon'] = json_obj['coordinates']['lng']
            yield item

            

                    

