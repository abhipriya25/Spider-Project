import scrapy
from locations.items import GeojsonPointItem
from locations.categories import Code
import pycountry
from scrapy import Selector
import uuid
from string import ascii_uppercase as auc
import re


class JammuAndKashmirBankDacSpider(scrapy.Spider):
    name = 'jammu_and_kashmir_bank_dac'
    brand_name = 'Jammu & Kashmir Bank'
    spider_type = 'chain'
    spider_chain_id = 2520
    spider_chain_name = 'Jammu & Kashmir Bank'
    spider_categories = [Code.BANK, Code.ATM]
    spider_countries = [pycountry.countries.lookup('ind').alpha_3]
    allowed_domains = ['www.jkbank.com']

    def start_requests(self):
        for i in auc:
            url = f'https://www.jkbank.com/others/common/responseBranch.php?branch={i}&color=green&optype=loc_brn_alpha'
            url_atm = f'https://www.jkbank.com/others/common/responseBranch.php?branch={i}&color=green&optype=atm_alpha'
            yield scrapy.Request(url, meta={'start_url': url, 'type': 'branch'}, callback=self.parse)
            yield scrapy.Request(url_atm, meta={'start_url': url_atm, 'type': 'atm'}, callback=self.parse)

    def format_time_from_12h_to24h(self, time):
        time = time.lower()
        time = time.split('to')
        time_start = time[0]
        time_end = time[1]
        time_start = time_start.replace(':', '.')
        time_end = time_end.replace(':', '.')
        time_list = []
        if 'a.m.' in time_start:
            time_start = time_start.replace('a.m.', 'am').replace(' ', '')
        if 'a.m.' in time_end:
            time_end = time_end.replace('a.m.', 'am').replace(' ', '')
        if 'p.m.' in time_start:
            time_start = time_start.replace('p.m.', 'pm').replace(' ', '')
        if 'p.m.' in time_end:
            time_end = time_end.replace('p.m.', 'pm').replace(' ', '')
        if 'am' in time_start:
            time_start = time_start.replace('am', '').replace('.', ':').replace(' ', '')
        if 'am' in time_end:
            time_end = time_end.replace('am', '').replace('.', ':').replace(' ', '')
        if 'pm' in time_start:
            time_start = time_start.replace('pm', '').replace(' ', '')
            time_start = time_start.split('.')
            time_start[0] = str(int(time_start[0]) + 12)
            time_start = ':'.join(time_start)
        if 'pm' in time_end:
            time_end = time_end.replace('pm', '').replace(' ', '')
            time_end = time_end.split('.')
            time_end[0] = str(int(time_end[0]) + 12)
            time_end = ':'.join(time_end)
        time_list.append(time_start)
        time_list.append(time_end)
        return time_list

    def parse_atms(self, response):
        name = ''
        email = ''
        if Selector(text=response.text).xpath('//tr[3]/td[2]/strong/text()').get() is not None:
            addr_full = Selector(text=response.text).xpath('//tr[3]/td[2]/strong/text()').get()
            if Selector(text=response.text).xpath('//tr[1]/td[2]/strong/text()').get() is not None:
                name = Selector(text=response.text).xpath('//tr[1]/td[2]/strong/text()').get()
            if Selector(text=response.text).xpath('//tr[4]/td[2]/a/text()').get() is not None:
                email = Selector(text=response.text).xpath('//tr[4]/td[2]/a/text()').get()
            store = {

                'chain_name': self.spider_chain_name,
                'chain_id': self.spider_chain_id,
                'brand': self.brand_name,
                'ref': uuid.uuid4().hex,
                'addr_full': addr_full,
                'website': 'https://www.jkbank.com/',
                'name': name,
                'email': email,
            }
            yield GeojsonPointItem(**store)

    def parse_branches(self, response):
        opening_hours = ''
        phone = ''
        email = ''
        hours_mo_sa = ''
        name = ''
        hours_su = ''
        lunch_time = ''
        if Selector(text=response.text).xpath('//tr[2]/td[2]/text()').get() is not None:
            addr_full = Selector(text=response.text).xpath('//tr[2]/td[2]/text()').get()
            if Selector(text=response.text).xpath('//tr[1]/td[2]/strong/text()').get() is not None:
                name = Selector(text=response.text).xpath('//tr[1]/td[2]/strong/text()').get()
            if Selector(text=response.text).xpath('//tr[4]/td[2]/text()').get() is not None:
                phone = Selector(text=response.text).xpath('//tr[4]/td[2]/text()').get()
            if 'Landline' in phone:
                phone = re.search('(?<=Landline:)(.*)', phone).group()
            phone = phone.replace('-', '')
            if '.' in phone:
                phone = phone.split('.')
            elif '/' in phone:
                phone = phone.split('/')
            else:
                phone = phone.split(',')
            if Selector(text=response.text).xpath('//tr[5]/td[2]/a/text()').get() is not None:
                email = Selector(text=response.text).xpath('//tr[5]/td[2]/a/text()').get()
            if Selector(text=response.text).xpath('//tr[10]/td[2]/text()').get() is not None:
                hours_mo_sa = Selector(text=response.text).xpath('//tr[10]/td[2]/text()').get()
            if Selector(text=response.text).xpath('//tr[12]/td[2]/text()').get() is not None:
                hours_su = Selector(text=response.text).xpath('//tr[12]/td[2]/text()').get()
            if Selector(text=response.text).xpath('//tr[14]/td[2]/text()').get() is not None:
                lunch_time = Selector(text=response.text).xpath('//tr[14]/td[2]/text()').get()

            if 'to' in hours_mo_sa:
                hours_mo_sa = self.format_time_from_12h_to24h(hours_mo_sa)
                if 'to' in lunch_time:
                    lunch_time = self.format_time_from_12h_to24h(lunch_time)
                    opening_hours = f'Mo-Sa {hours_mo_sa[0]}-{lunch_time[0]}, {lunch_time[1]}-{hours_mo_sa[1]};'
                else:
                    opening_hours = f'Mo-Sa {hours_mo_sa[0]}-{hours_mo_sa[1]};'

            if 'off' in hours_su.lower():
                hours_su = ' Su off; '
                opening_hours += hours_su

            elif 'to' in hours_su:
                hours_su = self.format_time_from_12h_to24h(hours_su)
                opening_hours += f' Su {hours_su[0]}-{hours_su[1]}; '

            opening_hours += 'Sa[2],Sa[4] off'

            store = {

                'ref': uuid.uuid4().hex,
                'chain_name': self.spider_chain_name,
                'chain_id': self.spider_chain_id,
                'brand': self.brand_name,
                'addr_full': addr_full,
                'website': 'https://www.jkbank.com/',
                'name': name,
                'phone': phone, #&&&&&
                'email': email,
                'opening_hours': opening_hours,
            }
            yield GeojsonPointItem(**store)

    def parse(self, response):

        branch_and_atms = Selector(text=response.text).xpath('//option[@value!="-1"]/@value').getall()
        for item in branch_and_atms:
            if response.meta['type'] == 'branch':
                url = f'https://www.jkbank.com/others/common/responseBranch.php?branch={item}&color=green&optype=brinfo'
                yield scrapy.Request(url, meta={'start_url': url}, callback=self.parse_branches)
            if response.meta['type'] == 'atm':
                url = f'https://www.jkbank.com/others/common/responseBranch.php?branch={item}&color=green&optype=atminfo'
                yield scrapy.Request(url, meta={'start_url': url}, callback=self.parse_atms)

