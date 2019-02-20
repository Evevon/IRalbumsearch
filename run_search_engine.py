import scrapy
from scrapy.crawler import CrawlerProcess
from albumscraper.spiders import nme_spider, pitchfork_spider, rollingstone_spider
from scrapy.settings import Settings
import albumscraper.settings as crawl_settings
from mapreduce import indexmusic, mr_settings


def crawl_data():
    crawler_settings = Settings()
    crawler_settings.setmodule(crawl_settings)

    # Distributed crawling of websites with spiders in parallel.
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(nme_spider.NmeSpider)
    process.crawl(pitchfork_spider.PitchforkSpider)
    process.crawl(rollingstone_spider.RollingstoneSpider)
    process.start()


def indexing():
    albumindexprocess = indexmusic.MusicIndexMapReduce(
                          mr_settings.default_input_dir, mr_settings.default_output_dir,
                          mr_settings.default_n_mappers, mr_settings.default_n_reducers)
    albumindexprocess.run()


#crawl_data()
indexing()
