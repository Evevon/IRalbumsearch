from django.shortcuts import render
from searchengine.scripts.indexfuncs import *
from searchengine.scripts.searchfuncs import *

def index(request):
    '''
    Return the homepage, and load search index if not yet loaded.
    '''
    # if search index is loaded, retrieve. else, load search index
    if 'searchindex' not in request.session:
        indices = loadsearchindex('m')
        request.session['searchindex'] = indices

    context = {}

    return render(request, 'searchengine/index.html', context)


def results(request):
    query = request.POST.get('searchquery')
    indices = request.session.get('searchindex')
    misspelled, query, searchresults = term_based_search(query, *indices, 2, 1)
    context = {'searchresults' : searchresults,
               'misspelled' : misspelled,
               'query' : query,
              }
    return render(request, 'searchengine/results.html', context)
