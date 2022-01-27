# -*- coding: utf-8 -*-
from cgitb import reset
from gc import callbacks
import scrapy
from locations.items import GeojsonPointItem
import re


class SportisimoSpider(scrapy.Spider):
    name = 'sportisimo_dac'
    allowed_domains = ['sportisimo.sk']
    start_urls = ['https://www.sportisimo.sk/predajne/slovensko']

    def parse(self, response):
        for link in response.css('div.select_options#store_list_select_country_popup a::attr(href)'):
            yield response.follow(link, callback=self.parse_page)


    def parse_page(self, response):
        name = response.css('div.sb_name a::text').getall()
        #ref = response.xpath('//div[@class="col"]/@id').getall()
        address = response.css('div.sb_name span::text').getall()  
        email = response.css('p.sb_email a::text').getall()
        country = response.css('div.select_header strong::text').get()
        opening_hours = response.css('p.sb_open::text').getall()
        #phone = response.xpath('//*[@id="mcetoc_1eron30fu1"]/a::text').get()
        
        
        data = [{'id':1, 'name':name[0], 'country':country, 'address':address[0], 'email':email[0], 'opening_hours':opening_hours[0],}]

        i = 1
        while i < len(name):
            data.append({'id':i, 'name':name[i], 'country':country, 'address':address[i], 'email':email[i], 'opening_hours':opening_hours[i],})
            i += 1


        for row in data:
            item = GeojsonPointItem()

            item['ref'] = row['id']
            item['name'] = row['name']
            item['brand'] = 'Sportisimo'
            item['addr_full'] = row['address']
            item['country'] = row['country']
            item['email'] = row['email']
            item['phone'] = '421220570870'
            item['website'] = 'https://www.sportisimo.sk'
            item['opening_hours'] = row['opening_hours']


            yield item