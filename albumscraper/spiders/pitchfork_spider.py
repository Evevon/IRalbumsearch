import scrapy
import json
import preprocessing
from urllib.parse import urljoin
from albumscraper.items import Album
from jsonwriter import write_to_json


class PitchforkSpider(scrapy.Spider):
    name = 'pitchfork_spider'
    allowed_domains = ['pitchfork.com']
    start_urls = ['https://pitchfork.com/reviews/albums/']
    count = 0
    COUNT_MAX = 2

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
        self.count = self.count + 1

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
        album['url'] = url
        album['name'] = name
        album['description'] = description

        data = {}        
        data['id'] = 'PF_' + str(self.count)
        data['url'] = url
        data['name'] = name
        data['description'] = description

        # path = '/Users/Friso/PycharmProjects/IRalbumsearch/data/'
        # filename = str(path + 'PF_' + str(self.count) + '.json')
        # with open(filename, 'w') as outfile:
        #     json.dump(data, outfile)

        write_to_json('PF_' + str(self.count) + '.json', self.count, data)

        yield album
