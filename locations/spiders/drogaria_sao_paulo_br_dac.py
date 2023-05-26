# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict
import re

class Drogaria_Sao_Paulo_BR_Spider(scrapy.Spider):

    name = "drogaria_sao_paulo_br_dac"
    brand_name = "Drogaria São Paulo"
    spider_type: str = "chain"
    spider_chain_id = 5498
    spider_chain_name = "Drogaria São Paulo"
    spider_categories: List[str] = [Code.DRUGSTORE_OR_PHARMACY, Code.PHARMACY]
    spider_countries: List[str] = [pycountry.countries.lookup('br').alpha_2]
    allowed_domains: List[str] = ['www.drogariasaopaulo.com.br']

    start_urls = ['https://www.drogariasaopaulo.com.br/api/dataentities/PR/documents/f52e9e7f-a02c-11ea-8337-0a8ac637298d/arquivo/attachments/nossas-lojas.js']

    def parse_hours(self,row):
        
        opening = ''

        if row.get("horarioAberturaSegsex"):
            opening += f'Mo-Fr {row["horarioAberturaSegsex"]}-{row["horarioFechamentoSegsex"]}; '

        if row.get("horarioAberturaSabado"):
            opening += f'Sa {row["horarioAberturaSabado"]}-{row["horarioFechamentoSabado"]}; '

        if row.get("horarioAberturaDomingo"):
            opening += f'Su {row["horarioAberturaDomingo"]}-{row["horarioFechamentoDomingo"]}; '
        
        return opening[:-2]

    def parse_phones(self,row):

        phones = []

        if row.get('telefoneUm'): phones.append(row['telefoneUm'])
        if row.get('telefoneDois'): phones.append(row['telefoneDois'])
        if row.get('whatsapp'): phones.append(row.get('whatsapp'))
        
        return phones

    def parse(self, response):

        responseData = response.json()

        for row in responseData["retorno"]:
    
            data = {
                'ref': row.get('id'),
                'chain_name': self.spider_chain_name,
                'chain_id': self.spider_chain_id,
                'brand': self.brand_name,
                'name': row.get('nome'),
                'addr_full': f'{row.get("cidade")}, {row.get("endereco")}, {row.get("uf")}, {row.get("cep")}',
                'city': row.get('cidade'),
                'state': row.get('uf'),
                'street': row.get('endereco'),
                'postcode': row.get('cep'),
                'country': self.spider_countries,
                'phone': self.parse_phones(row),
                'website': 'https://www.drogariasaopaulo.com.br',
                'opening_hours': self.parse_hours(row),
                'lat': float(re.sub(r',', '.', row.get('latitude'))) if row.get('latitude') else "",
                'lon': float(re.sub(r',', '.', row.get('longitude'))) if row.get('longitude') else "",
            }

            yield GeojsonPointItem(**data)