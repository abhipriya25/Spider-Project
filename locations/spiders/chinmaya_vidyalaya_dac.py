import scrapy
from locations.categories import Code
import pycountry
import uuid
import re
from locations.items import GeojsonPointItem
from scrapy import Selector


class ChinmayaVidyalayaDacSpider(scrapy.Spider):
    name = 'chinmaya_vidyalaya_dac'
    brand_name = 'Chinmaya Vidyalaya'
    spider_categories = [Code.SCHOOL]
    spider_countries = [pycountry.countries.lookup('in').alpha_2, pycountry.countries.lookup('bh').alpha_2,
                        pycountry.countries.lookup('my').alpha_2, pycountry.countries.lookup('us').alpha_2,
                        pycountry.countries.lookup('nz').alpha_2, pycountry.countries.lookup('lk').alpha_2,
                        pycountry.countries.lookup('id').alpha_2, pycountry.countries.lookup('mu').alpha_2,
                        pycountry.countries.lookup('hk').alpha_2, pycountry.countries.lookup('au').alpha_2,
                        pycountry.countries.lookup('ca').alpha_2, pycountry.countries.lookup('gb').alpha_2
                        ]
    spider_type = 'chain'
    spider_chain_id = 33931
    spider_chain_name = 'Chinmaya Vidyalaya'
    allowed_domains = ['www.chinmayamission.com']
    start_urls = ['https://www.chinmayamission.com/where-we-are/']

    def parse_centres(self, response):
        cntr = 0
        addr_full = ''
        city = ''
        country = ''
        site_url = ''
        phone = ''
        email = ''
        data = response.text
        name = Selector(text=data).xpath('//*[@id="ribbon-main"]/div[2]/h2/text()').get()
        for item in Selector(text=data).xpath('//*[@id="content"]/div[3]/div/div[1]/p').getall():
            cntr = cntr + 1
            if cntr < 5:
                addr_full = addr_full + item
            elif cntr == 5:
                city = item
            elif cntr == 6:
                country = item
            elif cntr == 7:
                site_url = Selector(text=item).xpath('//a/@href').get()
            phone = Selector(text=data).xpath('//div[@class="trust-quick"]/div/p[1]').get()
            email = Selector(text=data).xpath('//div[@class="trust-quick"]/div/p[2]').get()
            addr_full = re.sub('<.*?>', '', addr_full)
            city = re.sub('<.*?>', '', city)
            country = re.sub('<.*?>', '', country)
            if phone is not None:
                phone = re.sub('<.*?>', '', phone)
            if email is not None:
                email = re.sub('<.*?>', '', email)
            if phone is not None and '@' in phone:
                email = phone
                phone = ''
            if email is not None and '@' not in email:
                phone = phone + '/' + email
                if Selector(text=data).xpath('//div[@class="trust-quick"]/div/p[3]').get() is not None:
                    email = Selector(text=data).xpath('//div[@class="trust-quick"]/div/p[3]').get()
                    email = re.sub('<.*?>', '', email)
                else:
                    email = ''
            if phone is not None:
                phone = phone.replace('-', '').replace('+', '').replace('(', '').replace(')', '').replace(' ', '') \
                    .replace('Cell:', '').replace('Whatsapp', '').replace('Mo:', '').replace('Mob:', '').replace('PH.',
                                                                                                                 '').replace(
                    '&amp', '')
                if ';' in phone:
                    phone = phone.split(';')
                else:
                    phone = phone.split('/')
        if addr_full == '' and Selector(text=data).xpath('//*[@id="content"]/div[@class="fouthrow"]').get():
            cntr = 0
            for item in Selector(text=data).xpath('//*[@id="content"]/div[6]/div[2]/p').getall():
                cntr = cntr + 1
                if cntr < 4:
                    addr_full = addr_full + item
                elif cntr == 4:
                    item = item.split('-')
                    city = item[0]
                elif cntr == 5:
                    item = item.split(',')
                    country = item[1]
                elif cntr == 6:
                    phone = str(item)
                elif cntr == 7:
                    email = item
                site_url = Selector(text=data).xpath('//*[@id="content"]/div[6]/div[2]/a/@href').get()
            addr_full = re.sub('<.*?>', '', addr_full)
            city = re.sub('<.*?>', '', city)
            country = re.sub('<.*?>', '', country)
            phone = re.sub('<.*?>', '', phone)
            email = re.sub('<.*?>', '', email)
            phone = phone.replace('-', '').replace('+', '').replace('(', '').replace(')', '').replace(' ', '') \
                .replace('Cell:', '').replace('Whatsapp', '').replace('Mo:', '').replace('Mob:', '').replace('PH.',
                                                                                                             '').replace(
                '&amp', '')
            if ';' in phone:
                phone = phone.split(';')
            else:
                phone = phone.split('/')
        if addr_full != '':
        
            store_url = ""

            if site_url:
                site_url = site_url.replace(' ','')

                if len(site_url) > 10:
                    store_url = 'http://' + site_url if site_url[0] != 'h' else site_url

            store = {
                     'chain_name': self.spider_chain_name,
                     'chain_id': self.spider_chain_id,
                     'brand': self.brand_name,
                     'name': name,
                     'addr_full': addr_full,
                     'city': city,
                     'country': country,
                     'store_url': store_url,
                     'phone': phone,
                     'email': email,
                     'ref': uuid.uuid4().hex,
                     'website': 'https://www.chinmayamission.com/'}

            yield GeojsonPointItem(**store)

    def parse_trusts(self, response):
        cntr = 0
        addr_full = ''
        city = ''
        country = ''
        site_url = ''
        phone = ''
        email = ''
        data = response.text
        name = Selector(text=data).xpath('//*[@id="content"]/div[2]/h2/text()').get()
        for item in Selector(text=data).xpath('//*[@id="content"]/div[3]/div/div[1]/p').getall():
            cntr = cntr + 1
            if 5 > cntr > 1:
                addr_full = addr_full + item
            elif cntr == 5:
                city = item
            elif cntr == 7:
                country = item
            elif cntr == 8:
                site_url = item
            phone = Selector(text=data).xpath('//*[@id="content"]/div[3]/div/div[2]/div/p[1]').get()
            email = Selector(text=data).xpath('//*[@id="content"]/div[3]/div/div[2]/div/p[2]').get()
            addr_full = re.sub('<.*?>', '', addr_full)
            city = re.sub('<.*?>', '', city)
            country = re.sub('<.*?>', '', country)
            site_url = re.sub('<.*?>', '', site_url)
            site_url = site_url.replace('Website :', '')
            if phone is not None:
                phone = re.sub('<.*?>', '', phone)
            if email is not None:
                email = re.sub('<.*?>', '', email)
            if phone is not None and '@' in phone:
                email = phone
                phone = ''
            if email is not None and '@' not in email:
                phone = phone + '/' + email
                if Selector(text=data).xpath('//div[@class="trust-quick"]/div/p[3]').get() is not None:
                    email = Selector(text=data).xpath('//*[@id="content"]/div[3]/div/div[2]/div/p[3]').get()
                    email = re.sub('<.*?>', '', email)
                else:
                    email = ''
            if phone is not None:
                phone = phone.replace('-', '').replace('+', '').replace('(', '').replace(')', '').replace(' ', '') \
                    .replace('Cell:', '').replace('Whatsapp', '').replace('Mo:', '').replace('Mob:', '').replace('PH.',
                                                                                                                 '').replace(
                    '&amp', '')
                if ';' in phone:
                    phone = phone.split(';')
                else:
                    phone = phone.split('/')

        store_url = ""
        if site_url:

            site_url = site_url.replace(' ','')

            if len(site_url) > 10:
                store_url = 'http://' + site_url if site_url[0] != 'h' else site_url

        store = {


                 'chain_name': self.spider_chain_name,
                 'chain_id': self.spider_chain_id,
                 'brand': self.brand_name,
                 'name': name,
                 'addr_full': addr_full,
                 'city': city,
                 'country': country,
                 'store_url': store_url,
                 'phone': phone,
                 'email': email,
                 'ref': uuid.uuid4().hex,
                 'website': 'https://www.chinmayamission.com/'}

        yield GeojsonPointItem(**store)

    def parse_temples(self, response):
        cntr = 0
        addr_full = ''
        city = ''
        country = ''
        postcode = ''
        phone = ''
        phone_list = []
        email = ''
        data = response.text
        name = Selector(text=data).xpath('//*[@id="ribbon-main"]/div[2]/h2/text()').get()
        for item in Selector(text=data).xpath('//*[@id="content"]/div[4]/div[2]/p').getall():
            cntr = cntr + 1
            if 5 > cntr > 2:
                addr_full = addr_full + item
            elif cntr == 5:
                city = item
            elif cntr == 6:
                row_list = item.split(',')
                country = row_list[1]
            elif cntr == 8:
                postcode = item
            elif cntr == 9:
                if item is not None:
                    if '@' in item:
                        email = item
                    else:
                        phone = item
            elif cntr == 10:
                if item is not None:
                    email = item
            addr_full = re.sub('<.*?>', '', addr_full)
            city = re.sub('<.*?>', '', city)
            country = re.sub('<.*?>', '', country)
            postcode = re.sub('<.*?>', '', postcode)
            email = re.sub('<.*?>', '', email)
            phone = re.sub('<.*?>', '', phone)
            phone = phone.replace('+', '').replace('-', '').replace(' ', '')
            phone_list = phone.split('/')

        store = {
                 'chain_name': self.spider_chain_name,
                 'chain_id': self.spider_chain_id,
                 'brand': self.brand_name,
                 'name': name,
                 'addr_full': addr_full,
                 'city': city,
                 'country': country,
                 'phone': phone_list,
                 'postcode': postcode,
                 'email': email,
                 'ref': uuid.uuid4().hex,
                 'website': 'https://www.chinmayamission.com/'
                 }

        yield GeojsonPointItem(**store)

    def parse_ashrams(self, response):
        data = response.text
        name = Selector(text=data).xpath('//*[@id="ribbon-main"]/div[2]/h2/text()').get()
        cntr = 0
        addr_full = ''
        city = ''
        country = ''
        postcode = ''
        state = ''
        phone = ''
        phone_list = []
        email = ''
        for item in Selector(text=data).xpath('//*[@id="content"]/div[5]/div[1]/p').getall():
            cntr += 1
            if 5 > cntr > 2:
                addr_full = addr_full + item
            elif cntr == 6:
                city_postcode = item
                city_postcode = city_postcode.split('-')
                city = city_postcode[0]
                postcode = city_postcode[1]
            elif cntr == 7:
                state = item
            elif cntr == 8:
                country = item
            addr_full = re.sub('<.*?>', '', addr_full)
            city = re.sub('<.*?>', '', city)
            state = re.sub('<.*?>', '', state)
            country = re.sub('<.*?>', '', country)
            postcode = re.sub('<.*?>', '', postcode)

        if Selector(text=data).xpath('//*[@id="content"]/div[5]/div[2]/p[7]').get() is not None:
            if '@' in Selector(text=data).xpath('//*[@id="content"]/div[5]/div[2]/p[7]').get():
                email = Selector(text=data).xpath('//*[@id="content"]/div[5]/div[2]/p[7]').get()
            else:
                phone = Selector(text=data).xpath('//*[@id="content"]/div[5]/div[2]/p[7]').get()

            if Selector(text=data).xpath('//*[@id="content"]/div[5]/div[2]/p[8]').get() is not None:
                if '@' in Selector(text=data).xpath('//*[@id="content"]/div[5]/div[2]/p[8]').get():
                    email = Selector(text=data).xpath('//*[@id="content"]/div[5]/div[2]/p[8]').get()
                else:
                    phone = phone + '/' + Selector(text=data).xpath('//*[@id="content"]/div[5]/div[2]/p[8]').get()
            if Selector(text=data).xpath('//*[@id="content"]/div[5]/div[2]/p[9]').get() is not None:
                email = Selector(text=data).xpath('//*[@id="content"]/div[5]/div[2]/p[9]').get()

            email = re.sub('<.*?>', '', email)
            phone = re.sub('<.*?>', '', phone)
            phone = phone.replace('+', '').replace('-', '').replace(' ', '')
            phone_list = phone.split('/')

        store = {
                 'chain_name': self.spider_chain_name,
                 'chain_id': self.spider_chain_id,
                 'brand': self.brand_name,
                 'name': name,
                 'addr_full': addr_full,
                 'city': city,
                 'postcode': postcode,
                 'state': state,
                 'country': country,
                 'email': email,
                 'phone': phone_list,
                 'ref': uuid.uuid4().hex,
                 'website': 'https://www.chinmayamission.com/'
                 }

        yield GeojsonPointItem(**store)

    def parse(self, response):
        '''
            @url https://www.chinmayamission.com/where-we-are/
        '''
        centers = response.xpath('//*[@id="content"]/div[3]/div[3]/div[@class="where-div centre_block"]').get()
        for item in Selector(text=centers).xpath('//div').getall():
            url = Selector(text=item).xpath('//a/@href').get()
            if 'http' in url:
                yield scrapy.Request(url, meta={'start_url': url}, callback=self.parse_centres)

        trusts = response.xpath('//*[@id="content"]/div[3]/div[3]/div[@class="where-div trust_block"]').get()
        for item in Selector(text=trusts).xpath('//div').getall():
            url = Selector(text=item).xpath('//a/@href').get()
            if 'http' in url:
                yield scrapy.Request(url, meta={'start_url': url}, callback=self.parse_trusts)

        temples = response.xpath('//*[@id="content"]/div[3]/div[3]/div[@class="where-div temple_block"]').get()
        for item in Selector(text=temples).xpath('//div').getall():
            url = Selector(text=item).xpath('//a/@href').get()
            if 'http' in url:
                yield scrapy.Request(url, meta={'start_url': url}, callback=self.parse_temples)

        ashrams = response.xpath('//*[@id="content"]/div[3]/div[3]/div[@class="where-div ashram_block"]').get()
        for item in Selector(text=ashrams).xpath('//div').getall():
            url = Selector(text=item).xpath('//a/@href').get()
            url = 'https://www.chinmayamission.com' + url
            if 'where-we-are' in url:
                yield scrapy.Request(url, meta={'start_url': url}, callback=self.parse_ashrams)

