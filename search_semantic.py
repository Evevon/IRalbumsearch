from collections import Counter
from math import log10
import os
import json
from scipy import spatial
import time
import operator
from preprocessing import preprocess_text
from spellchecker import SpellChecker
import spacy

nlp = spacy.load('en_core_web_lg')


dir_ = os.path.dirname(os.path.abspath(__file__))
with open(dir_ + '/mapreduce/output_files/index.json') as f:
    index = json.load(f)

starttime = time.time()


def most_similar(word):  # function addapted from https://github.com/explosion/spaCy/issues/276
    queries = [w for w in word.vocab if w.is_lower == word.is_lower and w.prob >= -15]
    by_similarity = sorted(queries, key=lambda w: word.similarity(w), reverse=True)
    return by_similarity[1:4]
    

def term_based_search():
    query = 'best albums of 2019'

    #check spelling:
    spell = SpellChecker()
    corrected_query = [spell.correction(word) for word in query.split()]

    semantic_query = []
	for i in query.split():
    	semantic_query = semantic_query + ([w.lower_ for w in most_similar(nlp.vocab[str(i)])])

	print(semantic_query)

    query = preprocess_text(query)

    n = {url['doc_id'] for item in index.values() for url in item}
    n = len(n)

    query_tfidf = [(max(float(0), 1 + log10(count))) * (log10(n / len(index[word])))
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
