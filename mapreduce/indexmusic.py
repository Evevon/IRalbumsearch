from mapreduce.mapreduce import MapReduce
import sys
import mapreduce.mr_settings
from collections import Counter
from math import log10
import os

class MusicIndexMapReduce(MapReduce):
    def __init__(self, input_dir, output_dir, n_mappers, n_reducers):
        MapReduce.__init__(self, input_dir, output_dir, n_mappers, n_reducers)

    def mapper(self, doc_id, doc_content):
        """Map function for music indexing"""
        results = []
        # each word that appears in the document content gets as value the
        # document it is encountered.
        word_list = doc_content.split()
        word_count = Counter(word_list)
        for word in set(word_list):
            results.append((word, (doc_id, word_count[word])))
        return results

    def reducer(self, key, N, values_list):
        """Reducer function for music indexing"""
        # for each key word, return the document id's of the documents
        # in which the key word can be found. Add tf * idf value.
        df = len(values_list)
        idf = N/df
        for value in values_list:
            tf = value[1]
            value.append(tf * log10(idf))
        return values_list
