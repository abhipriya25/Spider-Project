# -*- coding: utf-8 -*-
import scrapy
from locations.items import GeojsonPointItem
from locations.categories import Code
import pycountry
import uuid
import re

class JarirBookstoreDacSpider(scrapy.Spider):
    name = 'jarir_bookstore_dac'
    brand_name = 'Jarir Bookstore'
    spider_type = 'chain'
    spider_chain_name = 'Jarir Bookstore'
    spider_chain_id = 29298
    spider_categories = [Code.BOOKSTORE]
    spider_countries = [pycountry.countries.lookup('sa').alpha_2, pycountry.countries.lookup('kw').alpha_2,
                        pycountry.countries.lookup('bh').alpha_2, pycountry.countries.lookup('qa').alpha_2, pycountry.countries.lookup('ae').alpha_2]
    allowed_domains = ['www.jarir.com']

    def start_requests(self):
        url_sa = f'https://www.jarir.com/api/master/store-locator-data?data=%7B%22type%22:%22centre%22,%22countryId%22:181,%22cityId%22:null%7D&storeCode=sa_ar'
        url_ku = 'https://www.jarir.com/api/master/store-locator-data?data={"type":"centre","countryId":109,"cityId":null}&storeCode=sa_ar'
        url_ba = 'https://www.jarir.com/api/master/store-locator-data?data={"type":"centre","countryId":17,"cityId":null}&storeCode=sa_ar'
        url_qa = 'https://www.jarir.com/api/master/store-locator-data?data={"type":"centre","countryId":169,"cityId":null}&storeCode=sa_ar'
        url_uae = 'https://www.jarir.com/api/master/store-locator-data?data={"type":"centre","countryId":214,"cityId":null}&storeCode=sa_ar'
        for url in [url_sa, url_ku, url_ba, url_qa, url_uae]:
            cntry = ''
            if url == url_sa:
                cntry = 'sa'
            elif url == url_ku:
                cntry = 'ku'
            elif url == url_ba:
                cntry = 'ba'
            elif url == url_qa:
                cntry = 'qa'
            elif url == url_uae:
                cntry = 'uae'
            yield scrapy.Request(
                url=url,
                method='GET',
                meta={'country': cntry},
                callback=self.parse,
            )

    def time_format(self, time):
        time = time.split('-')
        time_start = time[0]
        time_finish = time[1]
        if 'am' in time_start:
            time_start = time_start.replace('am', '').replace(' ', '')
            if ':' not in time_start:
                time_start = f'{time_start}:00'
        elif 'pm' in time_start or 'midnight' in time_start:
            time_start = time_start.replace('pm', '').replace(' ', '').replace('midnight', '')
            if ':' in time_start:
                time_start = time_start.split(':')
                time_start_h = time_start[0]
                time_start_h = int(time_start_h) + 12
                time_start = f'{str(time_start_h)}:{time_start[1]}'
            else:
                time_start = int(time_start) + 12
                time_start = f'{str(time_start)}:00'
        if 'am' in time_finish:
            time_finish = time_finish.replace('am', '')
            if ':' not in time_finish:
                time_finish = f'{time_finish}:00'
        elif 'pm' in time_finish or 'midnight' in time_finish:
            time_finish = time_finish.replace('pm', '').replace(' ', '').replace('midnight', '')
            if ':' in time_finish:
                time_finish = time_finish.split(':')
                time_finish_h = time_finish[0]
                time_finish_h = int(time_finish_h) + 12
                time_finish = f'{str(time_finish_h)}:{time_finish[1]}'
            else:
                time_finish = int(time_finish) + 12
                time_finish = f'{str(time_finish)}:00'
        return f'{time_start}-{time_finish}'

    def parse(self, response):
        '''
            @url https://www.jarir.com/api/master/store-locator-data?data=%7B%22type%22:%22centre%22,%22countryId%22:181,%22cityId%22:null%7D&storeCode=sa_ar
            @returns items 60 90
            @scrapes lat lon ref
        '''
        responseData = response.json()
        for item in responseData['data']:
            phone_list = []
            opening = ''
            phone = item['mobile_number']
            phone_list.append(phone)
            if response.meta['country'] == 'sa' or response.meta['country'] == 'qa' or response.meta['country'] == 'ku':
                opening = item['locales'][0]['timing_info']
                if opening == "Open 24 Hours":
                    opening = '24/7'
                else:
                    opening = opening.split('|')
                    sa_th = opening[0]
                    fr = opening[1]
                    sa_th = re.search('(?<=Thursday:)(.*)', sa_th).group()
                    sa_th = sa_th.lower()
                    fr = re.search('(?<=Friday: )(.*)', fr).group()
                    fr = fr.lower()
                    opening = f'Mo-Th {self.time_format(sa_th)}; Fr {self.time_format(fr)}; Sa-Su {self.time_format(sa_th)}'
            if response.meta['country'] == 'uae':
                opening = item['locales'][0]['timing_info']
                if opening == "Open 24 Hours":
                    opening = '24/7'
                else:
                    opening = opening.split('|')
                    if 'Wednesday' not in opening[0]:
                        su_th = opening[0]
                        fr_sa = opening[1]
                        su_th = re.search('(?<=Thursday :)(.*)', su_th).group()
                        su_th = su_th.lower()
                        fr_sa = re.search('(?<=Saturday : )(.*)', fr_sa).group()
                        fr_sa = fr_sa.lower()

                        print(opening)

                        opening = f'Mo-Th {self.time_format(su_th)}; Fr-Sa {self.time_format(fr_sa)}'
                    elif len(opening) == 3:
                        sa_we = opening[0]
                        th = opening[1]
                        fr = opening[2]
                        sa_we = re.search('(?<=Wednesday:)(.*)', sa_we).group()
                        sa_we = sa_we.lower()
                        th = re.search('(?<=Thursday: )(.*)', th).group()
                        th = th.lower()
                        fr = re.search('(?<=Friday:)(.*)', fr).group()
                        fr = fr.lower()
                        opening = f'Mo-We {self.time_format(sa_we)}; Th {self.time_format(th)}; Fr {self.time_format(fr)}; Sa-Su {self.time_format(sa_we)}'
                    else:
                        sa_we = opening[0]
                        th_fr = opening[1]
                        sa_we = re.search('(?<=Wednesday:)(.*)', sa_we).group()
                        sa_we = sa_we.lower()
                        th_fr = re.search('(?<=Friday : )(.*)', th_fr).group()
                        th_fr = th_fr.lower()
                        opening = f'Mo-We {self.time_format(sa_we)}; Th-Fr {self.time_format(th_fr)}; Sa-Su {self.time_format(sa_we)}'
            if response.meta['country'] == 'ba':
                opening = item['locales'][0]['timing_info']
                if opening == "Open 24 Hours":
                    opening = '24/7'
                else:
                    su_th = re.search('(?<=Thursday :)(.*)', opening).group()
                    su_th = su_th.lower()
                    opening = f'Mo-Su {self.time_format(su_th)}'

            store = {
                'chain_name': self.spider_chain_name,
                'chain_id': self.spider_chain_id,
                'brand': self.brand_name,
                'ref': uuid.uuid4().hex,
                'website': 'https://www.jarir.com/',
                'addr_full': item['default_centre_address'],
                'name': item['default_centre_name'],
                'postcode': item['default_postal_code'],
                'lat': item['latitude'],
                'lon': item['longitude'],
                'phone': phone_list,
                'opening_hours': opening
            }
            yield GeojsonPointItem(**store)
