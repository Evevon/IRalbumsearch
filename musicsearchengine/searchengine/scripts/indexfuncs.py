import os
import json


def loadsearchindex(size):
    print('loading search index')
    dir_ = os.path.dirname(os.path.abspath(__file__))
    with open('{}/title_index_{}.json'.format(dir_, size)) as f:
        title_index = json.load(f)
    with open('{}/content_index_{}.json'.format(dir_, size)) as f:
        content_index = json.load(f)

    return title_index, content_index
