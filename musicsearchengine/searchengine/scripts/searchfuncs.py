from searchengine.scripts.preprocessing import preprocess_text
from math import log10
import operator
from collections import Counter
from scipy import spatial
from datetime import datetime


def calc_idf(n, searchindex, word):
    try:
        idf = log10(n) / len(searchindex[word])
        return idf
    except KeyError:
        return 0

def term_based_search(query, searchindex):
    prep_query = preprocess_text(query)
    n = {url['doc_id'] for item in searchindex.values() for url in item}
    n = len(n)

    # tf idf for the query
    query_tfidf = [(max(float(0), 1 + log10(count))) * calc_idf(n, searchindex, word)
                    for word, count in Counter(prep_query).items()]

    # determine keyword vector for web page documents in database
    dict_docs = {}
    for j, word in enumerate(prep_query):
        if word not in searchindex:
            continue
        for i in searchindex[word]:
            if i['doc_id'] in dict_docs:
                dict_docs[i['doc_id']][0][j] = i['tfidf']
            else:
                doctitle = ' '.join(i['title'])
                dateobj = datetime.strptime(i['date'][0][:10], '%Y-%m-%d')
                date = dateobj.strftime('%B %d, %Y')
                dict_docs[i['doc_id']] = [[0 for _ in range(len(prep_query))],
                                          doctitle,
                                          date,
                                         ]
                dict_docs[i['doc_id']][0][j] = i['tfidf']

    # compute cosine similarity between web page documents and the query
    search_results = {}
    for key, valuelist in dict_docs.items():
        [document_tfidf, title, date] = valuelist
        search_results[key] = (1 - spatial.distance.cosine(query_tfidf, document_tfidf),
                               title,
                               date,
                              )

    sorted_results = sorted(search_results.items(), key=operator.itemgetter(1), reverse=True)

    return sorted_results[:10]
