from mapreduce.mapreduce import MapReduce
import sys
import mapreduce.mr_settings
from collections import Counter
from math import log10
from math import log
import os

class MusicIndexMapReduce(MapReduce):
    def __init__(self, input_dir, output_dir, n_mappers, n_reducers):
        MapReduce.__init__(self, input_dir, output_dir, n_mappers, n_reducers)

    def mapper(self, doc_id, title, word_list):
        """Map function for music indexing"""
        results = []
        # each word that appears in the document content gets as value the
        # document it is encountered.
        word_count = Counter(word_list)
        for word in set(word_list):
            results.append((word, {"doc_id": doc_id,
                                   "title": title,
                                   "count": word_count[word],
                                   }))
        return results

    def reducer(self, key, N, values_list):
        """Reducer function for music indexing"""
        # for each key word, return the document id's of the documents
        # in which the key word can be found. Add tf * idf value.
        df = len(values_list)
        idf = log10(N/df)
        for value in values_list:
            tf = max(0, 1 + log10(value["count"]))
            value["tfidf"] = tf * idf
        return values_list


class TitleIndexMapReduce(MapReduce):
    """MapReduce mapper and reducer for title index"""
    def __init__(self, input_dir, output_dir, n_mappers, n_reducers):
        MapReduce.__init__(self, input_dir, output_dir, n_mappers, n_reducers)

    def mapper(self, doc_id, title, pptitle, word_list):
        """Map function for music indexing"""
        results = []
        # each word that appears in the document title gets as value the
        # document it is encountered.
        word_count = Counter(pptitle)
        for word in set(pptitle):
            results.append((word, {"doc_id": doc_id,
                                   "title": title,
                                   "count": word_count[word],
                                   }))
        return results

    def reducer(self, key, N, values_list):
        """Reducer function for music indexing"""
        # for each key word, return the document id's of the documents
        # in which the key word can be found. Add tf * idf value.
        df = len(values_list)
        idf = log10(N/df)
        for value in values_list:
            tf = max(0, 1 + log10(value["count"]))
            value["tfidf"] = tf * idf
        return values_list
