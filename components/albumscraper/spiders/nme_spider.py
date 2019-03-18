import scrapy
import json
from urllib.parse import urljoin
from albumscraper.items import Album


class NmeSpider(scrapy.Spider):
    name = 'nme_spider'
    allowed_domains = ['www.nme.com']
    start_urls = ['https://www.nme.com/news/music/page/0']
    count = 0

    def parse(self, response):
        # collect all article links
        reviews = response.xpath('//a[@class="entry"]/@href').extract()
        # visit each album link and gather album info]

        for r in reviews:
            url = urljoin(response.url, r)
            yield scrapy.Request(url, callback=self.parse_album)

        # follow pagination links
        next_page = response.xpath("//link[@rel='next']/@href").extract_first()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_album(self, response):
        self.count = self.count + 1

        # extract info from each article
        name = response.xpath("//h1[@class='title-primary']//text()").extract_first()
        url = response.request.url
        description_list = response.xpath("//div[@class='articleBody']/p//text()").extract()
        date_published = response.xpath('//meta[@itemprop="datePublished"]/@content').extract()

        # text preprocessing
        description = ''.join(description_list)

        # create scrapy Item
        album = Album()
        album['id'] = 'NME_' + str(self.count)
        album['url'] = url
        album['name'] = name
        album['pptitle'] = name
        album['description'] = description
        album['date_published'] = date_published

        yield album
