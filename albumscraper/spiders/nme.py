import scrapy
from urllib.parse import urljoin
from albumscraper.items import Album


class AlbumSpider(scrapy.Spider):
    name = 'album_spider3'
    allowed_domains = ['www.nme.com']
    # start urls are the urls for multiple infinite-scroll pages
    start_urls = ['https://www.nme.com/news/music/page/'
                  + str(n) for n in range(0, 1000)]

    def parse(self, response):
        # collect all album links
        albums = response.xpath('//a[@class="entry"]/@href').extract()
        # visit each album link and gather album info
        for a in albums:
            url = urljoin(response.url, a)
            yield scrapy.Request(url, callback=self.parse_album)

    def parse_album(self, response):
        # extract info from html
        name = response.xpath(
          "//h1[@class='title-primary']//text()").extract_first()
        url = response.request.url
        description = response.xpath(
          "//div[@class='articleBody']//text()").extract()

        # create scrapy Item
        album = Album()
        album['name'] = name
        album['url'] = url
        album['description'] = description

        yield album
