# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import preprocessing
from jsonwriter import write_to_json
import json
import os
from textblob import TextBlob
import spacy


class AlbumscraperPipeline(object):
    def process_item(self, album, spider):

        dir_ = os.path.dirname(os.path.abspath(__file__))

        #sentiment and entity extraction
        #blob = album['description']

        #sentiment_blob = TextBlob(blob)
        #nlp = spacy.load('en')
        #entity_blob = nlp(blob)
        #entities = {X.text for X in entity_blob.ents if X.label_ == 'PERSON'}
        #entities = list(entities)

        #sentiment_dict = {'sentiment': sentiment_blob.sentiment[0], 'polarity': sentiment_blob.sentiment[1], 'entities': entities}

        #with open(dir_+ '/sentiment/' + spider.name + str(spider.count) + '_sentiment.json', 'w') as outfile:
        #  json.dump(sentiment_dict, outfile)

        # text preprocessing
        album['description'] = preprocessing.preprocess_text(album['description'])
        album['pptitle'] = preprocessing.preprocess_text(album['pptitle'])
        album['name'] = preprocessing.preprocess_text(
                          album['name'], specialchars=False,
                          stopwords=False, stem=False)

        # write scraped data to json file
        write_to_json(
          spider.name + str(spider.count) + '.json', spider.count, dict(album))

        return album
