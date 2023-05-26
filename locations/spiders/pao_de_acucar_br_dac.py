# -*- coding: utf-8 -*-

import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from typing import List, Dict
import re
import uuid

class Pao_De_Acucar_Spider(scrapy.Spider):

    name = "pao_de_acucar_br_dac"
    brand_name = "Pão de Açúcar"
    spider_type: str = "chain"
    spider_chain_id = 4051
    spider_chain_name = "Pão de Açúcar"
    spider_categories: List[str] = [Code.GROCERY]
    spider_countries: List[str] = [pycountry.countries.lookup('br').alpha_2]
    allowed_domains: List[str] = ['www.paodeacucar.com','s3.amazonaws.com']

    start_urls = ['https://s3.amazonaws.com/relacionamento.paodeacucar.com.br/localizador/store-locator-pa.json']

    def parse_hours(self, row):
        
        del_word = ['De','das','às','e', ',', 'a', 'as', 'das', 'de']
        
        days = {
            'segunda' : 'Mo',
            'Seg.' : 'Mo', 
            'seg' : 'Mo',
            'Dom.' : 'Su',
            'sábado' : 'Sa',
            'Domingos' : 'Su',
            'domingo' : 'Su',
            'sáb.' : 'Sa',
            'feriados' : '',
            'feriado' : '',
            'Fechada' : 'off',
            'fechada' : 'off'
        }
        
        r_normal = row['horario1'].replace('-',' ')
        r_special = row['horario2'].replace('-',' ')
        
        for i, j in days.items():
            r_normal = r_normal.replace(i, j)
            
        for i, j in days.items():
             r_special = r_special.replace(i, j)
        
        r_normal = re.sub(r'[^\w\s]','', r_normal) 
        r_special = re.sub(r'[^\w\s]','', r_special) 
        
        k1 = r_normal.split()
        k2 = r_special.split()
        
        m1 = []
        m2 = []
        
        for s in k1:
            if s not in del_word:
                m1.append(s)
        
        for s in k2:
            if s not in del_word:
                m2.append(s)
            
        nums = re.findall(r'\d+', r_normal)
        nums = [str(i) for i in nums]
        
        nums_s = re.findall(r'\d+', r_special)
        nums_s = [str(i) for i in nums_s]
        
        opening = ''
        
        print(nums,nums_s, m2)
        
        if m1 != []:
            
            opening += f"{m1[0]}-{m1[1]} {nums[0][:2]}:{nums[0][-2:]}-{nums[1][:2]}:{nums[1][-2:]}; "
            
        if m2 != []:
            
            if m2[0] == 'off':
                opening += f"Su,PH off"
            else:
                opening += f"{m2[0]}-{m2[0]} {nums_s[0][:2]}:{nums_s[0][-2:]}-{nums_s[1][:2]}:{nums_s[1][-2:]}; PH {nums_s[0][:2]}:{nums_s[0][-2:]}-{nums_s[1][:2]}:{nums_s[1][-2:]}"
        
        return opening

    def parse(self, response):

        responseData = response.json()

        for row in responseData:
    
            data = {
                'ref': uuid.uuid4().hex,
                'chain_name': self.spider_chain_name,
                'chain_id': self.spider_chain_id,
                'brand': self.brand_name,
                'name': row.get('nome'),
                'addr_full': f'{row.get("cidade")}, {row.get("bairro")}, {row.get("endereco")}',
                'city': row.get('cidade'),
                'street': row.get('endereco'),
                'phone': row.get('telefone'),
                'country': self.spider_countries,
                'website': 'https://www.paodeacucar.com',
                'opening_hours': self.parse_hours(row),
            }

            yield GeojsonPointItem(**data)