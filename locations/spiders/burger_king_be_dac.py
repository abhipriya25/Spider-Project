import scrapy
from locations.items import GeojsonPointItem
from locations.categories import Code
import pycountry
import uuid


class BurgerKingBelDacSpider(scrapy.Spider):
    name = 'burger_king_be_dac'
    brand_name = 'BURGER KING'
    spider_type = 'chain'
    spider_chain_id = "1498"
    spider_categories = [Code.FAST_FOOD]
    spider_countries = [
        pycountry.countries.lookup('be').alpha_3,
        pycountry.countries.lookup('lux').alpha_3
    ]
    allowed_domains = ['stores.burgerking.be']
    start_urls = ['https://stores.burgerking.be/api/v3/locations?fitAll=true&language=fr']

    def format_opening(self, times):
        mo_time = ''
        tu_time = ''
        we_time = ''
        th_time = ''
        fr_time = ''
        sa_time = ''
        su_time = ''
        for item in times:
            if item['startDay'] == 1:
                if item["closeTimeFormat"] == '00:00':
                    mo_time = f'{item["openTimeFormat"]}-24:00'
                else:
                    mo_time = f'{item["openTimeFormat"]}-{item["closeTimeFormat"]}'
            elif item['startDay'] == 2:
                if item["closeTimeFormat"] == '00:00':
                    tu_time = f'{item["openTimeFormat"]}-24:00'
                else:
                    tu_time = f'{item["openTimeFormat"]}-{item["closeTimeFormat"]}'
            elif item['startDay'] == 3:
                if item["closeTimeFormat"] == '00:00':
                    we_time = f'{item["openTimeFormat"]}-24:00'
                else:
                    we_time = f'{item["openTimeFormat"]}-{item["closeTimeFormat"]}'
            elif item['startDay'] == 4:
                if item["closeTimeFormat"] == '00:00':
                    th_time = f'{item["openTimeFormat"]}-24:00'
                else:
                    th_time = f'{item["openTimeFormat"]}-{item["closeTimeFormat"]}'
            elif item['startDay'] == 5:
                if item["closeTimeFormat"] == '00:00':
                    fr_time = f'{item["openTimeFormat"]}-24:00'
                else:
                    fr_time = f'{item["openTimeFormat"]}-{item["closeTimeFormat"]}'
            elif item['startDay'] == 6:
                if item["closeTimeFormat"] == '00:00':
                    sa_time = f'{item["openTimeFormat"]}-24:00'
                else:
                    sa_time = f'{item["openTimeFormat"]}-{item["closeTimeFormat"]}'
            elif item['startDay'] == 7:
                if item["closeTimeFormat"] == '00:00':
                    su_time = f'{item["openTimeFormat"]}-24:00'
                else:
                    su_time = f'{item["openTimeFormat"]}-{item["closeTimeFormat"]}'
        if mo_time == '':
            mo_time = 'off'
        if th_time == '':
            th_time = 'off'
        if tu_time == '':
            tu_time = 'off'
        if we_time == '':
            we_time = 'off'
        if fr_time == '':
            fr_time = 'off'
        if sa_time == '':
            sa_time = 'off'
        if su_time == '':
            su_time = 'off'
        return f'Mo {mo_time}; Tu {tu_time}; We {we_time}; Th {th_time}; Fr {fr_time}; Sa {sa_time}; Su {su_time}'

    def parse(self, response):
        '''
            @url https://stores.burgerking.be/api/v3/locations?fitAll=true&language=fr
            @returns items 50 80
            @scrapes lat lon ref
        '''
        responseData = response.json()

        for item in responseData:
            opening = self.format_opening(item['businessHours'])
            store = {
                'ref': uuid.uuid4().hex,
                'chain_name': "BURGER KING",
                'chain_id': "1498",
                'website': 'https://burgerking.be/',
                'addr_full': item['address']['fullAddress'],
                'city': item['address']['locality'],
                'street': item['address']['street'],
                'postcode': item['address']['zipCode'],
                'email': item['contact']['email'],
                'phone': [item['contact']['phone']],
                'store_url': item['contact']['url'],
                'opening_hours': opening,
                'lat': item['address']['latitude'],
                'lon': item['address']['longitude'],
            }

            yield GeojsonPointItem(**store)
