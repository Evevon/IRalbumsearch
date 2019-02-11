import scrapy
import json
from urllib.parse import urljoin
from albumscraper.items import Album


class AlbumSpider(scrapy.Spider):
    name = 'album_spider'
    allowed_domains = ['pitchfork.com']
    # start urls are the urls for multiple infinite-scroll pages
    start_urls = ['https://pitchfork.com/reviews/albums/?page='
                    + str(n) for n in range(1, 1000)]

    def parse(self, response):
         # collect all album links
         albums = response.xpath('//div[@class="review"]/a/@href').extract()
         # visit each album link and gather album info
         for a in albums:
             url = urljoin(response.url, a)
             yield scrapy.Request(url, callback=self.parse_album)

    def parse_album(self, response):
        # extract info from html
        name = response.xpath(
          "//h1[@class='single-album-tombstone__review-title']//text()").extract_first()
        url = response.request.url
        description_list = response.xpath(
          "//div[@class='contents dropcap']//text()").extract()

        # preprocessing some extracted info
        description = ''.join(description_list)

        # create scrapy Item
        album = Album()
        album['name'] = name
        album['url'] = url
        #album['description'] = description

        yield album
