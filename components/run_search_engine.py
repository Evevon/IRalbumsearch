"""
This file contains all the functionality of the music album search engine.
Running this file in the terminal will initialize the search engine.
"""

import os
import scrapy
from scrapy.crawler import CrawlerProcess
from albumscraper.spiders import nme_spider, pitchfork_spider, rollingstone_spider, theguardian_spider, uncut_spider
from scrapy.settings import Settings
import albumscraper.settings as crawl_settings
from mapreduce import indexmusic, mr_settings


def create_directories():
    num_mappers = mr_settings.default_n_mappers
    dir_ = os.path.dirname(os.path.abspath(__file__))
    if not os.path.exists(dir_ + '/'+ 'mapreduce/temp_map_files/'):
        os.makedirs(dir_ + '/' + 'mapreduce/temp_map_files/')
    if not os.path.exists(dir_ + '/'+ 'mapreduce/output_files/'):
            os.makedirs(dir_ + '/' + 'mapreduce/output_files/')
    for mapper in range(num_mappers):
        if not os.path.exists(dir_ + '/'+ 'mapreduce/input_files/' + str(mapper)):
            os.makedirs(dir_ + '/' + 'mapreduce/input_files/' + str(mapper))
    if not os.path.exists(dir_+ '/albumscraper/sentiment/'):
        os.makedirs(dir_+ '/albumscraper/sentiment/')


def crawl_data():
    crawler_settings = Settings()
    crawler_settings.setmodule(crawl_settings)

    # Distributed crawling of websites with spiders in parallel.
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(nme_spider.NmeSpider)
    process.crawl(pitchfork_spider.PitchforkSpider)
    process.crawl(rollingstone_spider.RollingstoneSpider)
    process.crawl(theguardian_spider.TheGuardianSpider)
    process.crawl(uncut_spider.UncutSpider)
    process.start()


def indexing():
    albumindexprocess = indexmusic.MusicIndexMapReduce(
                          mr_settings.default_input_dir, mr_settings.default_output_dir,
                          mr_settings.default_n_mappers, mr_settings.default_n_reducers)
    albumindexprocess.run("content")
    albumindexprocess = indexmusic.TitleIndexMapReduce(
                          mr_settings.default_input_dir, mr_settings.default_output_dir,
                          mr_settings.default_n_mappers, mr_settings.default_n_reducers)
    albumindexprocess.run("title")


create_directories()
crawl_data()
indexing()
