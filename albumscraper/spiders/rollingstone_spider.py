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

        # text preprocessing
        description = ''.join(description_list)
        description = preprocessing.preprocess_text(description)
        name = preprocessing.preprocess_text(
                name, specialchars=False, stopwords=False, stem=False)

        # create scrapy Item
        album = Album()
        album['url'] = url
        album['name'] = name
        album['description'] = description

        data = {}
        data['id'] = 'RS_' + str(self.count)
        data['url'] = url
        data['name'] = name
        data['description'] = description

        # path = '/Users/Friso/PycharmProjects/IRalbumsearch/data/'
        # filename = str(path + 'RS_' + str(self.count) + '.json')
        # with open(filename, 'w') as outfile:
        #     json.dump(data, outfile)

        write_to_json('RS_' + str(self.count) + '.json', self.count, data)

        yield album
