from mapreduce import MapReduce
import sys
import settings


class MusicIndex(MapReduce):
    def __init__(self, input_dir, output_dir, n_mappers, n_reducers):
        MapReduce.__init__(self, input_dir, output_dir, n_mappers, n_reducers)

    def mapper(self, doc_id, doc_content):
        """Map function for music indexing"""
        results = []
        # each word that appears in the document content gets as value the
        # document it is encountered.
        for word in set(doc_content.split()):
            results.append((word, doc_id))
        return results

    def reducer(self, key, values_list):
        """Reducer function for music indexing"""
        # for each key word, return the document id's of the documents
        # in which the key word can be found.
        return key, values_list


test = MusicIndex(settings.default_input_dir,
                        settings.default_output_dir,
                        settings.default_n_mappers,
                        settings.default_n_reducers)
test.run()
