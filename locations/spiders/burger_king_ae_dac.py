import scrapy
import pycountry
from locations.items import GeojsonPointItem
from locations.categories import Code
from bs4 import BeautifulSoup
import re
import uuid

class BurgerKing_UAE(scrapy.Spider):
    name = "burger_king_ae_dac"
    brand_name = 'BURGER KING'
    spider_type = 'chain'
    spider_chain_id = '1498'
    allowed_domains = ['uae.burgerking.me']
    start_urls = ["https://uae.burgerking.me"]
    spider_categories: list[str] = [Code.FAST_FOOD]
    spider_countries: list[str] = [pycountry.countries.lookup('ae').alpha_2]


    def start_requests(self):
        '''
        Spider entrypoint. 
        Request chaining starts from here.
        starting url gets the phone number
        calls back self.parse_contacts method

        yields HtmlResponse object
        '''
        url: str = "https://uae.burgerking.me/en/default.aspx"
        
        yield scrapy.Request(
            url=url,
            callback=self.parse_contacts
        )


    def parse_contacts(self, response):
        phone = [response.css('div.delivery').css('a').css('h2::text').get()]

        # url where the map data for shops is
        locationURL: str = "https://uae.burgerking.me/en/locations.aspx"

        yield scrapy.Request(
            locationURL,
            callback=self.parse,
            cb_kwargs=dict(phone=phone)
        )


    def parse(self, response, phone):
        '''
        yields the location of each shop as a dictionary

        @url https://uae.burgerking.me/en/locations.aspx
        @cb_kwargs {"phone": ["600-522-224"]}
        @returns items 88 88
        @returns requests 0
        @scrapes ref name lat lon addr_full phone
        '''

        # all the location data is in multiple div's with classname address
        locations: iter = response.css('div.address')

        for location in locations:
            name: str = location.css('p').css('strong::text').get().rstrip()
            # contains href of google maps
            coordinates_link: str = location.css('a').attrib['href']

            # retrieve lat and lon data from google maps link
            match_object: 're.Match' = re.search(r'(\d+\.?\d*),(\d+\.?\d*)', coordinates_link)
            lat: float
            lon: float
            lat, lon = match_object.group(1, 2)

            # using beautifulsoup because the website html contains nbsp; char which breaks xpath and scrapy css selectors
            # extracting them directly will require some tricks, beautifulsoup does it in a better way
            # albeit sacrificing some performance
            location_soup: BeautifulSoup = BeautifulSoup(location.extract(), 'html.parser')
            location_string_html_tag: tag = location_soup.find('p', class_='info')

            # stripped string returns an iterable of strings, string at index 0 contains the address of shop
            # usually gets a list of string with size 3, index 1 and 2 contain opening and closing times but data is empty
            address_string: str = str(list(location_string_html_tag.stripped_strings)[0])

            data: dict = {
                'ref': uuid.uuid4().hex,
                'chain_name': "BURGER KING",
                'chain_id': "1498",
                'name': name,
                'addr_full': address_string,
                'phone': phone,
                'website': 'https://uae.burgerking.me',
                'lat': lat,
                'lon': lon,
            }

            yield GeojsonPointItem(**data)
