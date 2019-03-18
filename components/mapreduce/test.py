import json
import os

def test_index():
    dir_ = os.path.dirname(os.path.abspath(__file__))
    with open("{}/output_files/index.json".format(dir_), 'r') as f:
        indexfile = json.load(f)
    for key in indexfile:
        titles = []
        for entry in indexfile[key]:
            titles.append(entry['title'])
        print("{}   :    {}\n".format(key, titles))

test_index()
