# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict
import json

class Big_HipermercadosSpider(scrapy.Spider):
    
    name = 'Big_Hipermercados_dac'
    brand_name = 'Big_Hipermercados'
    spider_type = 'chain'
    spider_chain_id = 21146
    spider_chain_name = 'BIG Hipermercados'
    spider_categories = [Code.GROCERY] 
    spider_countries: List[str] = [pycountry.countries.lookup('ind').alpha_3]
    allowed_domains: List[str] = ['www.grupobigbrasil.com.br','tabloide.big.com.br']
    
    def start_requests(self):
        url: str = "https://tabloide.big.com.br/api/v.5/lojas"
        payload = "bandeiras=8%2C15%2C13%2C6%2C5"
        
        yield scrapy.Request(
            url=url,
            method='POST',
            body=payload,
            callback=self.parse
        )

    def parse_hours(self,row):

      phones = []

      if len(row) > 20:

        row = row.replace('=>', ':')
        row = json.loads(row)

        if row != []:
          if row.get("CapitaisERegioesMetropolitanas"):
            phones.append(row.get("CapitaisERegioesMetropolitanas"))
          if row.get("DemaisLocalidades"):
            phones.append(row.get("DemaisLocalidades"))
          if row.get("AtendimentoUnico"):
            phones.append(row.get("AtendimentoUnico"))
      else:
        phones = row

      return phones
         
    def parse(self,response):
        responseData = response.json()

        for row in responseData['lojas']:

            data = {
                'ref': row['id'],
                'chain_name': self.spider_chain_name,
                'chain_id': self.spider_chain_id,
                'brand': self.brand_name,
                'addr_full': row.get("endereco", ""),
                'state': row.get('estado'),
                'city': row.get('cidade'),
                'phone': self.parse_hours(row.get('telefone')),
                'website': 'https://www.grupobigbrasil.com.br',
                'lat': -abs(float(row.get('latitude', ''))) if float(row.get('latitude', '')) > 10 else float(row.get('latitude', '')),
                'lon': float(row.get('longitude', '')),
            }

            yield GeojsonPointItem(**data)