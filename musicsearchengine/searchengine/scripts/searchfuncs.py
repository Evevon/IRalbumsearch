from searchengine.scripts.preprocessing import preprocess_text
from math import log10
import operator
from collections import Counter
from scipy import spatial

def term_based_search(query, searchindex):
    prep_query = preprocess_text(query)
    n = {url['doc_id'] for item in searchindex.values() for url in item}
    n = len(n)

    # tf idf for the query
    query_tfidf = [(max(float(0), 1 + log10(count))) * (log10(n) / len(searchindex[word]))
                    for word, count in Counter(prep_query).items()]

    # determine keyword vector for web page documents in database
    dict_docs = {}
    for j, word in enumerate(prep_query):
        for i in searchindex[word]:
            if i['doc_id'] in dict_docs:
                dict_docs[i['doc_id']][1][j] = i['tfidf']
            else:
                doctitle = ' '.join(i['title'])
                dict_docs[i['doc_id']] = [doctitle, [0 for _ in range(len(prep_query))]]
                dict_docs[i['doc_id']][1][j] = i['tfidf']

    # compute cosine similarity between web page documents and the query
    search_results = {}
    for key, valuelist in dict_docs.items():
        [title, document_tfidf] = valuelist
        search_results[key] = (1 - spatial.distance.cosine(query_tfidf, document_tfidf), title)

    sorted_results = sorted(search_results.items(), key=operator.itemgetter(1), reverse=True)
    print(sorted_results)

    return sorted_results[:10]




#    query = 'best albums of 2019'
#    query = preprocess_text(query)

#    n = {url['doc_id'] for item in index.values() for url in item}
#    n = len(n)

#    query_tfidf = [(max(float(0), 1 + log10(count))) * (log10(n) / len(index[word]))
#                   for word, count in Counter(query).items()]

#    dict_docs = dict()
#    for j, word in enumerate(query):
#        for i in index[word]:
#            if i['doc_id'] in dict_docs:
#                dict_docs[i['doc_id']][j] = i['tfidf']
#            else:
#                dict_docs[i['doc_id']] = [0] * len(query)
#                dict_docs[i['doc_id']][j] = i['tfidf']

#    search_results = dict()
#    for key, vector in dict_docs.items():
#        search_results[key] = (1 - spatial.distance.cosine(query_tfidf, vector))

#    sorted_x = sorted(search_results.items(), key=operator.itemgetter(1), reverse=True)
#    print(sorted_x[:20])
