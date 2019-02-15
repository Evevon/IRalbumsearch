import scrapy
import json
from urllib.parse import urljoin
from albumscraper.items import Album


class RollingstoneSpider(scrapy.Spider):
    name = 'nme_spider'
    allowed_domains = ['www.nme.com']
    start_urls = ['https://www.nme.com/news/music/page/0']

    def parse(self, response):
        # collect all article links
        reviews = response.xpath('//a[@class="entry"]/@href').extract()
        # visit each album link and gather album info
        for r in reviews:
            url = urljoin(response.url, r)
            yield scrapy.Request(url, callback=self.parse_album)

        # follow pagination links
        next_page = response.xpath("//link[@rel='next']/@href").extract_first()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_album(self, response):
        # extract info from each article
        name = response.xpath("//h1[@class='title-primary']//text()").extract_first()
        url = response.request.url
        detail = response.xpath("//div[@class='articleBody']//text()").extract()

        # print the result
        yield {'name': name, 'url': url}

        # preprocessing some extracted info
        # description = ''.join(detail)

        # create scrapy Item
        # album = Album()
        # album['name'] = name
        # album['url'] = url
        # album['description'] = description
