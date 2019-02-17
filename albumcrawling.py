import scrapy
from scrapy.crawler import CrawlerProcess
from albumscraper.spiders import nme_spider, pitchfork_spider, rollingstone_spider

# Distributed crawling of websites with spiders in parallel.
process = CrawlerProcess()
process.crawl(nme_spider.NmeSpider)
process.crawl(pitchfork_spider.PitchforkSpider)
process.crawl(rollingstone_spider.RollingstoneSpider)
process.start()
