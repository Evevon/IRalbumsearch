from collections import Counter
from math import log10
import os
import json
from scipy import spatial
import time
import operator
from preprocessing import preprocess_text

dir_ = os.path.dirname(os.path.abspath(__file__))
with open(dir_ + '/mapreduce/output_files/index.json') as f:
    index = json.load(f)

starttime = time.time()


def basic_search():
    query = 'best albums of 2019'
    query = preprocess_text(query)

    dict_docs = dict()
    for j, word in enumerate(query):
        for i in index[word]:
            if i['doc_id'] in dict_docs:
                dict_docs[i['doc_id']][j] = i['count']
            else:
                dict_docs[i['doc_id']] = [0] * len(query)
                dict_docs[i['doc_id']][j] = i['count']

    search_results = dict()
    for key, vector in dict_docs.items():
        search_results[key] = sum(vector)

    sorted_x = sorted(search_results.items(), key=operator.itemgetter(1), reverse=True)
    print(sorted_x[:20])


def term_based_search():
    query = 'best albums of 2019'
    query = preprocess_text(query)

    query_tfidf = [(max(float(0), 1 + log10(count))) * (log10(len(index) / len(index[word])))
                   for word, count in Counter(query).items()]

    dict_docs = dict()
    for j, word in enumerate(query):
        for i in index[word]:
            if i['doc_id'] in dict_docs:
                dict_docs[i['doc_id']][j] = i['tfidf']
            else:
                dict_docs[i['doc_id']] = [0] * len(query)
                dict_docs[i['doc_id']][j] = i['tfidf']

    search_results = dict()
    for key, vector in dict_docs.items():
        search_results[key] = (1 - spatial.distance.cosine(query_tfidf, vector))

    sorted_x = sorted(search_results.items(), key=operator.itemgetter(1), reverse=True)
    print(sorted_x[:20])


print(time.time() - starttime)

term_based_search()
