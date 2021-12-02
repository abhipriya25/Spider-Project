from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from locations import settings
from spiders.wilsonparking_dac import WilsonParkingSpider

from sys import argv

if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(WilsonParkingSpider)

    process.start()
