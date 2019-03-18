# -*- coding: utf-8 -*-
import scrapy
import json
from urllib.parse import urljoin
from albumscraper.items import Album
from jsonwriter import write_to_json
import os
from dateutil.parser import parse
from datetime import datetime

class UncutSpider(scrapy.Spider):
    name = 'uncut_spider'
    allowed_domains = ['uncut.co.uk']
    start_urls = ['https://www.uncut.co.uk/news/']
    count = 0

    def parse(self, response):
        # collect all article links
        reviews = response.xpath('//h2[@class="entry-title sub-heading"]/a/@href').extract()
        # visit each album link and gather album info

        # check if there are previously scraped file (i.e. no index created)
        path = os.path.abspath(__file__)
        if not os.path.isfile('/'.join(path.split('/')[:-3])+
            '/mapreduce/output_files/index.json'):

            # if no, scrape everything from scratch
            for r in reviews:
                url = urljoin(response.url, r)
                # then create a new one
                yield scrapy.Request(url,callback=self.parse_album)
        
        else:
            # otherwise check if content pages are updated
            for r in reviews:
                url = urljoin(response.url, r)   
                yield scrapy.Request(url,callback=self.check)

        # follow pagination links
        next_page = response.xpath("//a[contains(@class,'nextpostslink') and contains(@rel,'next')]/@href").extract_first()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url,callback=self.parse)

    def check(self, response):
        # check if the content page is updated
        date = response.xpath('//meta[@itemprop="dateModified"]/@content').extract()
        date = parse(date[0]).replace(tzinfo=None)
        # check the date where the index was last updated
        path = os.path.abspath(__file__)
        json_date = datetime.fromtimestamp(os.path.getmtime(
            '/'.join(path.split('/')[:-3])+'/mapreduce/output_files/index.json'))
        # if the last modified date of the content page is later than the last crawled date
        if date > json_date:
            yield scrapy.Request(response.url,callback=self.parse_album)

    def parse_album(self, response):
        self.count = self.count + 1

        # extract info from each article
        name = response.xpath("//title/text()").extract_first()
        url = response.request.url
        description_list = response.xpath(
        "//div[@itemprop='articleBody']//p//text()").extract()
        date_published = response.xpath("//meta[@itemprop='datePublished']/@content").extract()

        # text preprocessing
        description = ''.join(description_list)

        # create scrapy Item
        album = Album()
        album['id'] = 'UN_' + str(self.count)
        album['url'] = url
        album['name'] = name
        album['description'] = description
        album['date_published'] = date_published

        yield album

