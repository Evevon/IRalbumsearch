from django.shortcuts import render
from searchengine.scripts.indexfuncs import *
from searchengine.scripts.searchfuncs import *

def index(request):
    '''
    Return the homepage, and load search index if not yet loaded.
    '''
    # if search index is loaded, retrieve. else, load search index
    if 'searchindex' not in request.session:
        searchindex = loadsearchindex()
        request.session['searchindex'] = searchindex

    context = {}

    return render(request, 'searchengine/index.html', context)


def results(request):
    query = request.POST.get('searchquery')
    searchindex = request.session.get('searchindex')
    searchresults = term_based_search(query, searchindex)
    context = {'searchresults' : searchresults,
              }
    return render(request, 'searchengine/results.html', context)
