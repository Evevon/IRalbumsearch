import scrapy
from scrapy.crawler import CrawlerProcess
from albumscraper.spiders import nme_spider, pitchfork_spider, rollingstone_spider
from scrapy.settings import Settings
import albumscraper.settings as my_settings

crawler_settings = Settings()
crawler_settings.setmodule(my_settings)

# Distributed crawling of websites with spiders in parallel.
process = CrawlerProcess(settings=crawler_settings)
process.crawl(nme_spider.NmeSpider)
process.crawl(pitchfork_spider.PitchforkSpider)
process.crawl(rollingstone_spider.RollingstoneSpider)
process.start()
