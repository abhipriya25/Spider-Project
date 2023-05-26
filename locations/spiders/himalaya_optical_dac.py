import scrapy
from locations.items import GeojsonPointItem
from locations.categories import Code
import pycountry
import re
import uuid

class HimalayaOpticalDacSpider(scrapy.Spider):
    name = 'himalaya_optical_dac'
    brand_name = 'Himalaya Optical'
    spider_type = 'chain'
    spider_chain_id = 34183
    spider_chain_name = 'Himalaya Optical'
    spider_categories = [Code.OPTICAL]
    spider_countries = [pycountry.countries.lookup('ind').alpha_3]
    allowed_domains = ['cdn.shopify.com', 'himalayaoptical.com']
    start_urls = ['https://cdn.shopify.com/s/files/1/0426/8490/7673/t/2/assets/storeifyapps-geojson.js?v=102336522918373872421671093995']

    def parse_store(self, response):
        status = response.status
        opening_hours = ''
        if status == 200:
            monday_time = response.xpath('//tr[@class="row-mon"]/td/text()').get()
            if monday_time:
                if 'close' in monday_time.lower():
                    monday_time = 'off'

            tuesday_time = response.xpath('//tr[@class="row-tue"]/td/text()').get()
            if tuesday_time:
                if 'close' in tuesday_time.lower():
                    tuesday_time = 'off'

            wednesday_time = response.xpath('//tr[@class="row-wed"]/td/text()').get()
            if wednesday_time:
                if 'close' in wednesday_time.lower():
                   wednesday_time = 'off'

            thursday_time = response.xpath('//tr[@class="row-thu"]/td/text()').get()
            if thursday_time:
                if 'close' in thursday_time.lower():
                    thursday_time = 'off'

            friday_time = response.xpath('//tr[@class="row-fri"]/td/text()').get()
            if friday_time:
                if 'close' in friday_time.lower():
                   friday_time = 'off'

            saturday_time = response.xpath('//tr[@class="row-sat"]/td/text()').get()
            if saturday_time:
                if 'close' in saturday_time.lower():
                   saturday_time = 'off'

            sunday_time = response.xpath('//tr[@class="row-sun"]/td/text()').get()
            if sunday_time:
                if 'close' in sunday_time.lower():
                    sunday_time = 'off'

            if monday_time != 'off' or tuesday_time != 'off' or wednesday_time != 'off' or thursday_time != 'off' \
                    or friday_time != 'off' or saturday_time != 'off' or sunday_time != 'off':
                opening_hours = f'Mo {monday_time}; Tu {tuesday_time}; We {wednesday_time}; Th {thursday_time};' \
                                f' Fr {friday_time}; Sa {saturday_time}; Su {sunday_time}'

        store = {'ref': uuid.uuid4().hex,
                 'chain_name': self.spider_chain_name,
                 'chain_id': self.spider_chain_id,
                 'brand': self.brand_name,
                 'opening_hours': opening_hours,
                 'website': 'https://himalayaoptical.com/',
                 'store_url': response.meta['store_url'],
                 'addr_full': response.meta['addr_full'],
                 'name': response.meta['name'],
                 'phone': response.meta['phone'],
                 'email': response.meta['email'],
                 'lat': response.meta['lat'],
                 'lon': response.meta['lon'],
                 'state': response.meta['state'],
                 'city': response.meta['city']
                 }
        yield GeojsonPointItem(**store)

    def parse(self, response):
        '''
        @url https://cdn.shopify.com/s/files/1/0426/8490/7673/t/2/assets/storeifyapps-geojson.js?v=102336522918373872421671093995
        @returns items 120 140
        @scrapes addr_full lat lon
        '''
        responseData = response.text.split('properties:')
        for item in responseData:
            if 'category' in item:
                name = ''
                store_url = ''
                addr_full = ''
                phone_list = []
                email = ''
                lon = ''
                lat = ''
                state = ''
                city = ''
                if re.search('(?<=name:")(.*)(?=",thumbnai)', item) is not None:
                    name = re.search('(?<=name:")(.*)(?=",thumbnai)', item).group()
                if re.search('(?<=address:")(.*)(?=",phone)', item) is not None:
                    addr_full = re.search('(?<=address:")(.*)(?=",phone)', item).group()
                if re.search('(?<=phone:")(.*)(?=",email)', item) is not None:
                    phone = re.search('(?<=phone:")(.*)(?=",email)', item).group()
                    phone = phone.replace('-', '').replace(' ', '')
                    phone_list.append(phone)
                if re.search('(?<=email:")(.*)(?=",web)', item) is not None:
                    email = re.search('(?<=email:")(.*)(?=",web)', item).group()
                if re.search('(?<=lat:")(.*)(?=",lng)', item) is not None:
                    lat = re.search('(?<=lat:")(.*)(?=",lng)', item).group()
                if re.search('(?<=lng:")(.*)(?=",social)', item) is not None:
                    lon = re.search('(?<=lng:")(.*)(?=",social)', item).group()
                if re.search('(?<=country:")(.*)(?=",city)', item) is not None:
                    state = re.search('(?<=country:")(.*)(?=",city)', item).group()
                if re.search('(?<=city:")(.*)(?="}})', item) is not None:
                    city = re.search('(?<=city:")(.*)(?="}})', item).group()
                if re.search('(?<=url:")(.*)(?=",address)', item) is not None:
                    store_url = re.search('(?<=url:")(.*)(?=",address)', item).group()
                    store_url = 'https://himalayaoptical.com' + store_url

                    yield scrapy.Request(store_url, callback=self.parse_store,
                                             meta={'website': 'https://himalayaoptical.com/',
                                                   'store_url': store_url,
                                                   'addr_full': addr_full,
                                                   'name': name,
                                                   'phone': phone_list,
                                                   'email': email,
                                                   'lat': lat,
                                                   'lon': lon,
                                                   'state': state,
                                                   'city': city,
                                                   'handle_httpstatus_all': True,
                                                   'dont_retry': True,
                                                   })

