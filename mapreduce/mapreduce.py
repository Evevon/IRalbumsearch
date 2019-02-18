"""
This file implements a mapreduce framework in Python.
Code in this file is based on mapcakes: https://github.com/nidhog/mapcakes
"""


import settings
import json
import os
from multiprocessing import Process
from collections import defaultdict


class MapReduce(object):
    """
    MapReduce class representing the mapreduce model
    note: the 'mapper' and 'reducer' methods must be
    implemented to use the mapreduce model.
    """
    def __init__(self, input_dir = settings.default_input_dir,
                 output_dir = settings.default_output_dir,
                 n_mappers = settings.default_n_mappers,
                 n_reducers = settings.default_n_reducers,
                 clean = True):
        """
        :param input_dir: directory of the input files,
        taken from the default settings if not provided
        :param output_dir: directory of the output files,
        taken from the default settings if not provided
        :param n_mappers: number of mapper threads to use,
        taken from the default settings if not provided
        :param n_reducers: number of reducer threads to use,
        taken from the default settings if not provided
        :param clean: optional, if True temporary files are
        deleted, True by default.
        """
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.n_mappers = n_mappers
        self.n_reducers = n_reducers
        self.clean = clean

    def mapper(self, key, value):
        """
        outputs a list of key-value pairs, where the key is
        potentially new and the values are of a potentially
        different type.
        Note: this function is to be implemented.
        :param key:
        :param value:
        """
        pass

    def reducer(self, key, values_list):
        """
        Outputs a single value together with the provided key.
        Note: this function is to be implemented.
        :param key:
        :param value_list:
        """
        pass

    def check_position(self, key, position):
        """Checks if we are on the right position"""
        return position == (hash(key) % self.n_reducers)

    def run_mapper(self, index):
        """
        Runs the implemented mapper
        :param index: the index of the thread to run on
        """
        # open the current file according to the index
        f = open(settings.get_input_file(index), "r")
        # read the document ID
        doc_id = f.readline()
        # read the document content
        doc_content = f.read()
        # get the result of the mapper
        mapper_result = self.mapper(doc_id, doc_content)
        # store the result to be used by the reducer
        # reducer is determined by hash value of the key
        for reducer_index in range(self.n_reducers):
            temp_map_file = open(settings.get_temp_map_file(index, reducer_index), 'w+')
            json.dump([(indexword, doc_id) for (indexword, doc_id) in mapper_result
                            if self.check_position(indexword, reducer_index)],
                        temp_map_file)
            temp_map_file.close()

    def run_reducer(self, index):
        """
        Runs the implemented reducer
        :param index: the index of the thread to run on
        """
        key_values_map = defaultdict(list)
        # load the results of the map
        for mapper_index in range(self.n_mappers):
            temp_map_file = open(settings.get_temp_map_file(mapper_index, index), 'r')
            mapper_results = json.load(temp_map_file)
            # for each key reduce the values
            for (key, value) in mapper_results:
                key_values_map[key].append(value)
            temp_map_file.close()
            # remove temporary file
            if self.clean:
                os.unlink(settings.get_temp_map_file(mapper_index, index))
        # store the results for this reducer
        key_value_list = []
        for key in key_values_map:
            key_value_list.append(self.reducer(key, key_values_map[key]))
        output_file = open(settings.get_output_file(index), 'w+')
        json.dump(key_value_list, output_file)
        output_file.close()

    def run(self):
        """Executes the map and reduce operations"""
        # initialize mappers list
        map_workers = []
        # initialize reducers list
        rdc_workers = []
        # run the map step
        for thread_id in range(self.n_mappers):
            p = Process(target=self.run_mapper, args=(thread_id,))
            p.start()
            map_workers.append(p)
        [t.join() for t in map_workers]
        # run the reduce step
        for thread_id in range(self.n_reducers):
            p = Process(target=self.run_reducer, args=(thread_id,))
            p.start()
            rdc_workers.append(p)
        [t.join() for t in rdc_workers]
        # generate concatenated output file
        indexlist = []
        for reducer_index in range(self.n_reducers):
            reduce_file = open(settings.get_output_file(reducer_index), 'r')
            indexlist += json.load(reduce_file)
            reduce_file.close()
            if self.clean:
                os.unlink(settings.get_output_file(reducer_index))

        f = open(settings.get_output_join_file(), 'w+')
        json.dump(indexlist, f)
