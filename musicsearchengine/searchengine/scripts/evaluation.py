import searchfuncs as sfc
import indexfuncs as ifc


def evaluate(size, t_weight, c_weight):
    t_index, c_index = ifc.loadsearchindex(size)
    queries = ['Ariana Grande',
               'red hot chili peppers',
               'Head above water',
               'best albums of 2018',
               'upcoming artist',
               'music festivals',
               'Hip hop',
               'Jazz albums',
               'Music videos',
               'Bruce springsteen',
               'Lady Gaga',
               'British songs',
               'concerts in London',
               'Troye Sivan',
               'Met Gala',
               'Grammys',
               'Korean pop',
               'Rap',
               'Shallow soundtrack',
               'Billboard number 1 hits',
              ]
    result_collection = {}
    for query in queries:
        print(query)
        _a, _b, results = sfc.term_based_search(query, t_index, c_index, t_weight, c_weight)
        results = [(details[1], url) for (url, details) in results]
        q_result = {query: results}
        result_collection.update(q_result)

    return result_collection
