# -*- coding: utf-8 -*-
import scrapy
import json
import preprocessing
from urllib.parse import urljoin
from albumscraper.items import Album
from jsonwriter import write_to_json


class RollingstoneSpider(scrapy.Spider):
    name = 'rollingstone_spider'
    allowed_domains = ['rollingstone.com']
    start_urls = ['https://www.rollingstone.com/music/music-album-reviews/']
    count = 0

    def parse(self, response):
        # collect all article links
        reviews = response.xpath('//article[@class="c-card c-card--domino"]/a/@href').extract()
        # visit each album link and gather album info

        for r in reviews:
            url = urljoin(response.url, r)
            yield scrapy.Request(url, callback=self.parse_album)

        # follow pagination links
        next_page = response.xpath("//link[@rel='next']/@href").extract_first()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url,callback=self.parse)

    def parse_album(self, response):
        self.count = self.count + 1

        # extract info from each article
        name = response.xpath("//title/text()").extract_first()
        url = response.request.url
        description_list = response.xpath(
          """//meta[contains(@class,'swiftype') and contains(@name,'body')
          and contains(@data-type,'text')]/@content""").extract()
        date_published = response.xpath(
            """//meta[contains(@class,'swiftype') and contains(@name,'published_at')
            and contains(@data-type,'date')]/@content""").extract()

        # text preprocessing
        description = ''.join(description_list)

        # create scrapy Item
        album = Album()
        album['id'] = 'RS_' + str(self.count)
        album['url'] = url
        album['name'] = name
        album['pptitle'] = name
        album['description'] = description
        album['date_published'] = date_published


        yield album
