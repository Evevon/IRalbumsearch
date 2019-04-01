from django.shortcuts import render
from searchengine.scripts.indexfuncs import *
from searchengine.scripts.searchfuncs import *

def index(request):
    '''
    Return the homepage, and load search index if not yet loaded.
    '''
    # if search index is loaded, retrieve. else, load search index
    if 'searchindex' not in request.session:
        indices = loadsearchindex('c')
        request.session['searchindex'] = indices

    context = {}

    return render(request, 'searchengine/index.html', context)


def results(request):
    query = request.POST.get('searchquery')
    indices = request.session.get('searchindex')
    misspelled, query, searchresults = term_based_search(query, *indices, 2, 1)
    newresults = []
    for r in searchresults:
        r_detail_list = list(r[1])
        sent = r_detail_list[3]
        if sent > 0.2:
            sentword = 'Very Positive'
            r_detail_list.append('VP')
        elif sent > 0.05:
            sentword = 'Mildly Positive'
            r_detail_list.append('MP')
        elif sent > -0.05:
            sentword = 'Neutral'
            r_detail_list.append('NE')
        elif sent > -0.2:
            sentword = 'Mildly Negative'
            r_detail_list.append('MN')
        else:
            sentword = 'Very Negative'
            r_detail_list.append('VN')
        r_detail_list[3] = sentword
        newresults.append([r[0], r_detail_list])
    context = {'searchresults' : newresults,
               'misspelled' : misspelled,
               'query' : query,
              }
    return render(request, 'searchengine/results.html', context)
