import scrapy
import json
import preprocessing
from urllib.parse import urljoin
from albumscraper.items import Album


class PitchforkSpider(scrapy.Spider):
    name = 'pitchfork_spider'
    allowed_domains = ['pitchfork.com']
    start_urls = ['https://pitchfork.com/reviews/albums/']

    def parse(self, response):
        # collect all album links
        reviews = response.xpath('//div[@class="review"]/a/@href').extract()
        # visit each album link and gather album info
        for r in reviews:
            url = urljoin(response.url, r)
            yield scrapy.Request(url, callback=self.parse_album)

        # follow pagination links
        next_page = response.xpath(
            "//link[contains(@data-react-helmet,'true') and contains(@rel,'next')]/@href").extract_first()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url,callback=self.parse)

    def parse_album(self, response):
        # extract info from html
        name = response.xpath(
          "//h1[@class='single-album-tombstone__review-title']//text()").extract_first()
        url = response.request.url
        description_list = response.xpath(
          "//div[@class='contents dropcap']//text()").extract()

        # text preprocessing
        description = ''.join(description_list)
        description = preprocessing.preprocess_text(description)
        name = preprocessing.preprocess_text(
                name, specialchars=False, stopwords=False, stem=False)

        # create scrapy Item
        album = Album()
        album['name'] = name
        album['url'] = url
        album['description'] = description

        yield album
