import json
import os
from mapreduce.mr_settings import default_n_mappers


def write_to_json(filename, num, dict_):
    num_mappers = default_n_mappers
    dir_ = os.path.dirname(os.path.abspath(__file__))

    folder_num = str(num % num_mappers)
    print('directory:', dir_ + '/' + 'mapreduce/input_files/' + folder_num + '/' + filename)
    with open(dir_ + '/' + 'mapreduce/input_files/' + folder_num + '/' + filename, 'w') as outfile:
        json.dump(dict_, outfile)
