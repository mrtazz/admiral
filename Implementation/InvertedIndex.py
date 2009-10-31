"""
@file InvertedIndex.py
@brief creating inverted indexes and manage them for search
@author Daniel Schauenberg <schauend@informatik.uni-freiburg.de>
@version 0.1
@date 2009-10-24
"""

import pickle
from operator import itemgetter

class IndexManager:
    """ Class for managing the complete index

        this class manages an inverted index in a simple
        hash map of the form

        index = {
                    key : documents
                }
        where key is the word and documents is an array with
        the document IDs
    """
    index = {}

    def add_key(self, key, doc):
        """ method to add a document to a index object
            or create a new object

            Parameters:
                key -- the keyword to add to the index
                doc -- the document id to add
        """
        key = key.lower().replace("\n","")
        if (self.index.has_key(key)):
            if doc not in self.index[key]:
                self.index[key].append(doc)
                self.index[key].sort()
        else:
            entry = [doc]
            self.index[key] = entry

    def get_documents(self,key):
        """ method to get documents which contain the given
            key

            Parameters:
                key -- the keyword to get the documents for

            Returns:
                array of document IDs for the given key
        """
        return self.index[key.lower()]

    def get_intersected_list(self,keywords):
        """ method to get the intersected documents list for
            the keywords provided in the array

            Parameters:
                keywords -- array of keywords to search for

            Returns:
                intersected list of keywords
        """
        comparelist = self.get_documents(keywords.pop(0))
        intersected_list = []
        for key in keywords:
            docs = self.get_documents(key)
            matches = filter(lambda m: m in comparelist,docs)
            intersected_list.extend(matches)
        return intersected_list

    def get_index_size(self):
        """ method to get length of the index

            Returns:
                length of index
        """
        return len(self.index)

    def get_index(self):
        """ get the index object
        """
        return self.index

    def get_two_word_one_doc(self):
        """ O(n^2) implementation to find exactly one document to contain
            two words.
        """
        result = []
        for i in self.index.keys():
            for u in self.index.keys():
                intlist = self.get_intersected_list([i,u])
                if (len(intlist) == 1):
                    result.append([intlist[0],i,u])
        return result

    def write_object_to_disk(self,filepath,obj=None):
        """ method to write the object to the provided filepath

            Parameters:
                filepath -- file to write the index to
        """
        if (obj==None): obj = self.index

        try:
            f = open(filepath, 'w')
            pickle.dump(obj, f)
        except:
            pass

    def read_object_from_disk(self,filepath,ret=False):
        """ method to read object from file

            Parameters:
                filepath -- file to read index from
        """
        try:
            f = open(filepath, 'r')
            loaded_object = pickle.load(f)
        except:
            pass
        if (ret==False): self.index = loaded_object
        else: return loaded_object

    def get_word_frequencies(self):
        """ create object with frequencies of word occurrences

            Returns:
                dictionary with word occurrences, sorted
        """
        occurrences = {}
        for key in self.index.keys():
            occurrences[key] = len(self.index[key])
        sorted_occurrences = sorted(occurrences.items(), key=itemgetter(1))
        return sorted_occurrences
