# -*- coding: utf-8 -*-
import scrapy
import json
import preprocessing
from urllib.parse import urljoin
from albumscraper.items import Album
from jsonwriter import write_to_json


class TheGuardianSpider(scrapy.Spider):
    name = 'theguardian_spider'
    allowed_domains = ['theguardian.com']
    start_urls = ['https://www.theguardian.com/music+tone/albumreview/']
    count = 0

    def parse(self, response):
        # collect all album links
        reviews = response.xpath('//h3[@class="fc-item__title"]/a/@href').extract()
        # visit each album link and gather album info

        for r in reviews:
            url = urljoin(response.url, r)
            yield scrapy.Request(url, callback=self.parse_album)

        # follow pagination links
        next_page = response.xpath(
          "//a[contains(@class,'button button--small button--tertiary pagination__action--static ') and contains(@rel,'next')]/@href").extract_first()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url,callback=self.parse)

    def parse_album(self, response):
        self.count = self.count + 1

        # extract info from html
        name = response.xpath(
          "//title/text()").extract_first()
        url = response.request.url
        description_list = response.xpath(
          "//div[@class='content__article-body from-content-api js-article__body']//text()").extract()
        date_published = response.xpath("//time[@itemprop='datePublished']/@datetime").extract()

        # text preprocessing
        description = ''.join(description_list)

        # create scrapy Item
        album = Album()
        album['id'] = 'TG_' + str(self.count)
        album['url'] = url
        album['name'] = name
        album['pptitle'] = name
        album['description'] = description
        album['date_published'] = date_published

        yield album
