import scrapy
from urllib.parse import urljoin
from albumscraper.items import Album


class AlbumSpider(scrapy.Spider):
    name = 'album_spider2'
    allowed_domains = ['www.allmusic.com']
    # start urls are the urls for multiple infinite-scroll pages
    start_urls = ['https://www.allmusic.com/blog/lists-2/'
                  + str(n) for n in range(0, 10, 10)]

    def parse(self, response):
        # collect all album links
        albums = response.xpath('//div[@class="article-info"]/a/@href').extract()
        # visit each album link and gather album info
        for a in albums:
            url = urljoin(response.url, a)
            yield scrapy.Request(url, callback=self.parse_album)

    def parse_album(self, response):
        # extract info from html
        name = response.xpath(
          "//h1[@class='title']//text()").extract_first()
        url = response.request.url
        description = response.xpath(
          "//div[@class='article-body']//text()").extract()

        # create scrapy Item
        album = Album()
        album['name'] = name
        album['url'] = url
        album['description'] = description

        yield album
