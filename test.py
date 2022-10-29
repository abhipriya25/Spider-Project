import requests
import pandas as pd
import scrapy
from locations.categories import Code
import pycountry


#
url = "https://vxpim.visionexpress.in/pim/pimresponse.php/?service=storelocator&store=1"
#
payload = {}
headers = {
    'lat': '42.66519',
    'lon': '17.1071373'
}

response = requests.request("GET", url, headers=headers, data=payload)

a = response.json()
# b= a['result']
# for item in b:
#     print(item['address'])
#     print(item['postcode'])
#     print(item['city'])
#     print(item['state'])
#     print(item['store_phone'])
#     print(item['store_timing'])
#     print(item['lat'])
#     print(item['lng'])
#
data = response.json()['result']
df = pd.DataFrame(data)
#
# df.to_csv('visionexpress.csv')
#
# df.head()

class FortizoSpider(scrapy.Spider):
    name = "visionexpress_dac"
    brand_name = "Visionexpress"
    spider_type = "chain"
    spider_categories = [Code.SPECIALTY_STORE]
    spider_countries = [pycountry.countries.lookup('gr').alpha_3]
    allowed_domains = ["visionexpress.gr", "visionexpress.eu"]

    start_urls = ["https://www.visionexpress.in/findstore"]