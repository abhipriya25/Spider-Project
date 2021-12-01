from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from locations import settings
from spiders.sovcombank_dac import SovcombankSpider

from sys import argv

if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(SovcombankSpider)

    process.start()
