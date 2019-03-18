"""
This file implements a mapreduce framework in Python.
Code in this file is based on mapcakes: https://github.com/nidhog/mapcakes
"""


import mapreduce.mr_settings as settings
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
    def __init__(self, dir, input_dir = settings.default_input_dir,
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
        self.N = self.get_n_documents()

        print(self.N)

    def mapper(self, values):
        """
        outputs a list of key-value pairs, where the key is
        potentially new and the values are of a potentially
        different type.
        Note: this function is to be implemented.
        :param key:
        :param value:
        """
        pass

    def reducer(self, key, N, values_list):
        """
        Outputs a single value together with the provided key.
        Note: this function is to be implemented.
        :param key:
        :param value_list:
        """
        pass

    def get_n_documents(self):
        """outputs an integer denoting the amount of input documents."""
        dir_ = os.path.dirname(os.path.abspath(__file__))
        pathname = "{}/input_files/".format(dir_)
        amount_of_files = 0
        for dir_index in range(self.n_mappers):
            amount_of_files += len(os.listdir(pathname + "/" + str(dir_index)))

        return amount_of_files

    def check_position(self, key, position):
        """Checks if we are on the right position"""
        return position == (hash(key) % self.n_reducers)

    def run_mapper(self, map_index):
        """
        Runs the implemented mapper
        :param index: the index of the thread to run on
        """
        # open the files in the right directory according to the index
        dir_ = os.path.dirname(os.path.abspath(__file__))
        file_list = os.listdir('{}/input_files/{}'.format(dir_, map_index))
        mapper_result = []
        for file in file_list:
            # load file information
            with open('{}/input_files/{}/{}'.format(dir_, map_index, file), "r") as f:
                doc = json.load(f)
                # get the result of the mapper
                mapper_result.extend(self.mapper(doc))

        # store the result to be used by the reducer
        # reducer is determined by hash value of the key
        for reducer_index in range(self.n_reducers):
            filename = '{}/temp_map_files/map_file_{}-{}.json'.format(dir_, map_index, reducer_index)
            if os.path.exists(filename):
                mode = 'a' # append if already exists
            else:
                mode = 'w' # make a new file if not
            with open(filename, mode) as temp_map_file:
                json.dump([(indexword, doc['url']) for (indexword, doc['url']) in mapper_result
                                if self.check_position(indexword, reducer_index)],
                            temp_map_file)

    def run_reducer(self, index):
        """
        Runs the implemented reducer
        :param index: the index of the thread to run on
        """
        dir_ = os.path.dirname(os.path.abspath(__file__))
        key_values_map = defaultdict(list)
        # load the results of the map
        for mapper_index in range(self.n_mappers):
            filename = '{}/temp_map_files/map_file_{}-{}.json'.format(dir_, mapper_index, index)
            with open(filename, 'r') as temp_map_file:
                mapper_results = json.load(temp_map_file)
                # for each key reduce the values
                for (key, value) in mapper_results:
                    key_values_map[key].append(value)

            # remove temporary file
            if self.clean:
                os.unlink(filename)

        # store the results for this reducer
        key_value_list = {}
        for key in key_values_map:
            key_value_list[key] = self.reducer(key, self.N, key_values_map[key])

        with open('{}/output_files/reduce_file_{}.json'.format(dir_, index), 'w+') as output_file:
            json.dump(key_value_list, output_file)

    def run(self, indextype):
        """Executes the map and reduce operations"""
        dir_ = os.path.dirname(os.path.abspath(__file__))
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
        indexlist = {}
        for reducer_index in range(self.n_reducers):
            filename = '{}/output_files/reduce_file_{}.json'.format(dir_,reducer_index)
            reduce_file = open(filename, 'r')
            indexlist.update(json.load(reduce_file))
            reduce_file.close()
            if self.clean:
                os.unlink(filename)

        with open('{}/output_files/{}_index.json'.format(dir_, indextype), 'w+') as f:
            json.dump(indexlist, f)
