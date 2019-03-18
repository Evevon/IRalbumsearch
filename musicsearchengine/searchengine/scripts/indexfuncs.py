import os
import json


def loadsearchindex():
    print('loading search index')
    dir_ = os.path.dirname(os.path.abspath(__file__))
    with open(dir_ + '/testindex.json') as f:
        searchindex = json.load(f)

    return searchindex
