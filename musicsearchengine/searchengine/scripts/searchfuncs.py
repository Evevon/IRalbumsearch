from searchengine.scripts.preprocessing import preprocess_text
from math import log10
import operator
from collections import Counter
from scipy import spatial
from datetime import datetime
from spellchecker import SpellChecker
from copy import deepcopy

def get_keyword_vectors(index, prep_query):
    urlcollection = set()
    doc_dict = {}
    for doclist in index.values():
        for doc in doclist:
            # get doc values
            doc_id = doc['doc_id']
            doc_title = ' '.join(doc['title'])
            dateobj = datetime.strptime(doc['date'][0][:10], '%Y-%m-%d')
            date = dateobj.strftime('%B %d, %Y')
            sentiment = doc['sentiment']

            # add values to collections
            urlcollection.add(doc_id)
            doc_dict[doc_id] = {'keyvec' : [0 for _ in range(len(prep_query))],
                                'doc_title': doc_title,
                                'date': date,
                                'sentiment': sentiment,
                                }

    return urlcollection, doc_dict


def calc_idf(n, searchindex, word):
    try:
        idf = log10(n) / len(searchindex[word])
        return idf
    except KeyError:
        return 0


def fill_keyword_vectors(prep_query, searchindex, doc_dict):
    # determine keyword vector for web page documents in database
    for j, word in enumerate(prep_query):
        print(word)
        if word not in searchindex:
            continue
        for i in searchindex[word]:
            doc_dict[i['doc_id']]['keyvec'][j] = i['tfidf']

    return doc_dict


def term_based_search(query, t_index, c_index, t_weight, c_weight):
    # spell-check query
    misspelled, newquery = spellcheck_query(query)

    print(newquery)

    # preprocess query
    print('preprocess query')
    prep_query = preprocess_text(query)
    urlcollection1, doc_dict1 = get_keyword_vectors(t_index, prep_query)
    urlcollection2, doc_dict2 = get_keyword_vectors(c_index, prep_query)

    urlcollection = urlcollection1 | urlcollection2
    doc_dict1.update(doc_dict2)
    doc_dict = doc_dict1
    n = len(urlcollection)

    # tf idf for the query
    print('calculate tfidf')
    t_query_tfidf = [(max(float(0), 1 + log10(count))) * calc_idf(n, t_index, word)
                    for word, count in Counter(prep_query).items()]
    c_query_tfidf = [(max(float(0), 1 + log10(count))) * calc_idf(n, c_index, word)
                    for word, count in Counter(prep_query).items()]

    # get keyword vectors for document title and content
    title_vec_base = deepcopy(doc_dict)
    content_vec_base = deepcopy(doc_dict)
    print('get keyword vec title')
    title_keyword_vectors = fill_keyword_vectors(prep_query, t_index, title_vec_base)
    print('get keyword vec content')
    content_keyword_vectors = fill_keyword_vectors(prep_query, c_index, content_vec_base)

    # compute cosine similarity between web page documents and the query
    print('execute search')
    search_results = {}
    zerovec = [0 for _ in range(len(prep_query))]
    for key in title_keyword_vectors:
        title_tfidf = title_keyword_vectors[key]['keyvec']
        content_tfidf = content_keyword_vectors[key]['keyvec']
        title = title_keyword_vectors[key]['doc_title']
        date = title_keyword_vectors[key]['date']
        sentiment = title_keyword_vectors[key]['sentiment']

        # Get cosine values
        if title_tfidf == zerovec:
            t_cosine = 0
        else:
            t_cosine = 1 - spatial.distance.cosine(t_query_tfidf, title_tfidf)
        if content_tfidf == zerovec:
            c_cosine = 0
        else:
            c_cosine = 1 - spatial.distance.cosine(c_query_tfidf, content_tfidf)
        combined_cosine = (t_cosine * t_weight + c_cosine * c_weight) / (t_weight + c_weight)
        search_results[key] = (combined_cosine,
                               title,
                               date,
                               sentiment,
                              )

    sorted_results = sorted(search_results.items(), key=operator.itemgetter(1), reverse=True)

    return misspelled, newquery, sorted_results[:10]


def spellcheck_query(query):
    spell = SpellChecker()
    query_misspelled = False
    newquery = []

    for word in query.split():
        checked_word = spell.correction(word)
        if checked_word != word:
            query_misspelled = True
        newquery.append(checked_word)

    newquery = ' '.join(newquery)

    return query_misspelled, newquery
