# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import preprocessing
from jsonwriter import write_to_json


class AlbumscraperPipeline(object):
    def process_item(self, album, spider):
        # text preprocessing
        album['description'] = preprocessing.preprocess_text(album['description'])
        album['name'] = preprocessing.preprocess_text(
                          album['name'], specialchars=False,
                          stopwords=False, stem=False)

        # write scraped data to json file
        write_to_json(
          spider.name + str(spider.count) + '.json', spider.count, dict(album))

        return album
