"""
@file InvertedIndex.py
@brief creating inverted indexes and manage them for search
@author Daniel Schauenberg <schauend@informatik.uni-freiburg.de>
@version 0.1
@date 2009-10-24
"""

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
        """
        if (self.index[key]):
            if doc not in self.index[key]:
                self.index[key].append(doc)
                self.index[key].sort()
        else:
            self.index[key].append(doc)
            self.index[key].sort()

    def get_documents(self,key):
        """ method to get documents which contain the given
            key
        """
        return self.index[key]

    def get_intersected_list(self,keywords):
        """ method to get the intersected documents list for
            the keywords provided in the array
        """
