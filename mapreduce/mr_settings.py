"""
This file describes the settings for a mapreduce framework in Python.
Code in this file is based on mapcakes: https://github.com/nidhog/mapcakes
"""


# set default directory for the input files
default_input_dir = "input_files"
# set default directory for the temporary map files
default_temp_dir = "temp_map_files"
# set default directory for the output files
default_output_dir = "output_files"
# set default number for the map and reduce threads
default_n_mappers = 4
default_n_reducers = 4


# return the name of the input file
def get_input_file( index, input_dir = default_input_dir, extension = ".txt"):
    return "{}/file{}{}".format(input_dir, index, extension)


# return the name of the temporary map file corresponding to the given index
def get_temp_map_file(index, reducer, output_dir = default_temp_dir, extension = ".json"):
    return "{}/map_file_{}-{}{}".format(output_dir, str(index), str(reducer), extension)


# return the name of the output file given its corresponding index
def get_output_file(index, output_dir = default_output_dir, extension = ".json"):
    return "{}/reduce_file_{}{}".format(output_dir, str(index), extension)


# return the name of the output file
def get_output_join_file(output_dir = default_output_dir, extension = ".json"):
    return "{}/output{}".format(output_dir, extension)
