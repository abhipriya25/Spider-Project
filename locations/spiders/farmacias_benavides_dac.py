import scrapy
<<<<<<< HEAD
from locations.categories import Code
import pycountry
import re
import uuid
from locations.items import GeojsonPointItem

class FarmaciasBenavidesDacSpider(scrapy.Spider):
    name = 'farmacias_benavides_dac'
    brand_name = 'Farmacias Benavides'
    spider_type = 'chain'
    spider_categories = [Code.PHARMACY]
    spider_countries = [pycountry.countries.lookup('mx').alpha_3]
    allowed_domains = ['www.benavides.com.mx']
    start_urls = ['https://www.benavides.com.mx/_next/data/a69hWY2aIiREhDxCla97F/sucursales.json']

    # This part of the code formats the time to the open street map format
    # form the format in the json that uses a.m and p.m times. Some of the data
    # is in the format hh:mm:ss and here its being converted to hh:mm.
    def cleanAndFormatTime(self, time_open, time_close):
        if time_open == '24 hrs':
            return 'Mo-Fr 00:00-24:00;'
        elif ':' in time_open:
            if 'p' in time_open or 'P' in time_open:
                time_open = ''.join((re.findall(r'[0-9:]', time_open)))
                time_open = time_open.split(':')
                time_open[0] = int(time_open[0]) + 12
                time_open[0] = str(time_open[0])
                time_open = time_open[0] + ':' + time_open[1]
            else:
                time_open = ''.join((re.findall(r'[0-9:]', time_open)))
                time_open = time_open.split(':')
                time_open = time_open[0] + ':' + time_open[1]
            if 'p' in time_close or 'P' in time_close:
                time_close = ''.join((re.findall(r'[0-9:]', time_close)))
                time_close = time_close.split(':')
                time_close[0] = int(time_close[0]) + 12
                time_close[0] = str(time_close[0])
                time_close = time_close[0] + ':' + time_close[1]
            else:
                time_close = ''.join((re.findall(r'[0-9:]', time_close)))
                time_close = time_close.split(':')
                time_close = time_close[0] + ':' + time_close[1]
            return f'Mo-Fr {time_open}-{time_close};'

    def parse(self, response):
        '''
        @url https://www.benavides.com.mx/_next/data/a69hWY2aIiREhDxCla97F/sucursales.json
        @returns items 1100 1200
        @scrapes addr_full lat lon
        '''
        responseData = response.json()

        for item in responseData['pageProps']['maplocations']:
            opening = ''
            if item.get('Do_open') == '24 hrs' and item.get('Lu_vi_open') == '24 hrs' and item.get(
                    'Sa_open') == '24 hrs':
                opening = '24/7'
            else:
                if self.cleanAndFormatTime(item.get('Lu_vi_open'), item.get('Lu_vi_close')) is not None:
                    opening = opening + self.cleanAndFormatTime(item.get('Lu_vi_open'), item.get('Lu_vi_close'))

                if self.cleanAndFormatTime(item.get('Sa_open'), item.get('Sa_close')) is not None:
                    opening = opening + self.cleanAndFormatTime(item.get('Sa_open'), item.get('Sa_close'))

                if self.cleanAndFormatTime(item.get('Do_open'), item.get('Do_close')) is not None:
                    opening = opening + self.cleanAndFormatTime(item.get('Do_open'), item.get('Do_close'))

            store = {'ref': uuid.uuid4().hex,
                     'name': item.get('Branch_Name'),
                     'addr_full': f"{item.get('Branch_Street')} {item.get('Branch_Number')}, {item.get('Branch_Colonia')}, {item.get('Branch_City')}, {item.get('Branch_State')}, {item.get('Branch_Zip')}",
                     'street': item.get('Branch_Street'),
                     'city': item.get('Branch_City'),
                     'state': item.get('Branch_State'),
                     'postcode': item.get('Branch_Zip'),
                     'website': 'www.benavides.com.mx',
                     'lat': item.get('Branch_Latitud'),
                     'lon': item.get('Branch_Longitude'),
                     'opening_hours': opening
                     }

            yield GeojsonPointItem(**store)
=======
from bs4 import BeautifulSoup
import json
from locations.items import GeojsonPointItem
import numpy as np


#get baseurl in postman
class Farmacias_Benavides_Spider(scrapy.Spider):
    name = 'farmacias_benavides_dac'
    allowed_domains = ['www.benavides.com.mx/']
    spider_type: str = 'chain'

    def start_requests(self):


        baseurl = 'https://farmacias-benavides-prod.ent.eastus2.azure.elastic-cloud.com/api/as/v1/engines/benavides-locations/search.json?query='

        lista_zip = list(np.arange(20000,83000,2))
        #add zipcodes to baseurl and put them into a list
        links=[]

        for zip in lista_zip:
            url = baseurl + str(zip)
            links.append(url)
        cant_links = len(links)
        #for every link get data
        pp_lista = []

        for link in links:
            yield scrapy.Request(
            url=link,
            headers={'Connection':'keep-alive','user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
                            'authorization':'Bearer search-14h9b6oj7d5zdh5qy8k7a8yb'},
                            callback=self.parse
            )

    def parse(self,response):
        soup = BeautifulSoup(response.text,"html.parser")
   
        data = json.loads(str(soup))
        data_len = len(data['results'])
            
        for i in range(data_len):

                        item = GeojsonPointItem()
                        item['ref'] = data['results'][i]['local_id']['raw']
                        try:
                            item['name'] = data['results'][i]['branch_name']['raw']
                        except KeyError:
                            item['name'] = np.nan
                        try:
                            item['addr_full'] = data['results'][i]['branch_street']['raw']
                        except KeyError:
                            item['addr_full'] = np.nan
                        try:
                            item['postcode'] = data['results'][i]['branch_zip']['raw']
                        except KeyError:
                            item['postcode'] = np.nan
                        try:
                            item['city'] = data['results'][i]['branch_city']['raw']
                        except:
                            item['city'] = np.nan
                        try:
                            item['phone'] = data['results'][i]['branch_phone']['raw']
                        except KeyError:
                            item['phone'] = np.nan
                        try:
                            item['lat'] = (data['results'][i]['branch_latitud']['raw']).replace(',','.')

                        except:
                            item['lat'] = np.nan
                        
                        try:
                            item['lon'] = (data['results'][i]['branch_longitude']['raw']).replace(',','.')

                        except KeyError:
                            item['lon'] = np.nan

                        try:
                            if data['results'][i]['lu_vi_open']['raw'] == "24 hrs":
                                item['opening_hours']= '24 hs'
                            else:
                                item['opening_hours']= 'Mon Fri:' + data['results'][i]['lu_vi_open']['raw'] + '-' + data['results'][i]['lu_vi_close']['raw'] + ' Sa:' + data['results'][i]['sa_open']['raw'] + '-' + data['results'][i]['sa_close']['raw']
                        except KeyError: 
                            item['opening_hours']= np.nan


                        yield item
>>>>>>> lucasgil9084
