import scrapy
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