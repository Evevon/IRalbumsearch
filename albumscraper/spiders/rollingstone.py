# -*- coding: utf-8 -*-
import scrapy
import json
from urllib.parse import urljoin
from albumscraper.items import Album
import numpy as np

# text processing
import re
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS as sw
from nltk.stem import PorterStemmer


class RollingstoneSpider(scrapy.Spider):
    name = 'review_spider'
    allowed_domains = ['rollingstone.com']
    start_urls = ['https://www.rollingstone.com/music/music-album-reviews/']

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
        # extract info from each article
        name = response.xpath("//title/text()").extract_first()
        url = response.request.url
        detail = response.xpath(
            """//meta[contains(@class,'swiftype') and contains(@name,'body') 
            and contains(@data-type,'text')]/@content""").extract()

        # text preprocessing
        detail = np.array(detail)    
        detail = [word.rstrip() for word in detail] # remove all trailing white spaces
        detail = re.sub(r'[^a-zA-Z0-9\s]', "", str(detail)).lower()  # remove special characters, lowercase
        detail = [word for word in detail.split() if word not in (sw)]  # remove stopwords
        ps = PorterStemmer()
        detail = ' '.join([ps.stem(word) for word in detail])   # stemming

        # print the result
        yield {'name':name, 'url':url, 'detail':detail}

        # create scrapy Item
        #album = Album()
        #album['name'] = name
        #album['url'] = url
        #album['description'] = description
        