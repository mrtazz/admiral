"""
@file InvertedIndex.py
@brief creating inverted indexes and manage them for search
@author Daniel Schauenberg <schauend@informatik.uni-freiburg.de>
@version 0.1
@date 2009-10-24
"""

import heapq
import FileParser
from math import log
from operator import itemgetter

class IndexManager:
    """ Class for managing the complete index

        this class manages an inverted index in a simple
        hash map of the form

        index = {
                    key : documents
                }
        where key is the word and documents is also a hash
        map containing the document id and term frequency
        in the form of

        document = {
                        doc  : scores
                   }
        scores = {
                    'tf' : value,
                    'tf.idf' ; value
                 }
    """
    def __init__(self,folder):
        """ Constructor which creates the index and the set to hold
            the actual filenames
        """
        self.index = {}
        self.filenames = {}
        self.parser = FileParser.DocumentParser(folder)
        self.doc_count = self.parser.get_documents_count()

    def build_index(self):
        """ method to build the inverted index for the
            documents in the given folder. the file parser
            object is used to parse the single files.
        """
        docs = self.parser.get_documents()
        for d in docs:
            docid,words = self.parser.parse_file(d)
            for w in words:
                self.add_key(w,docid,d)

    def add_key(self, key, doc, filename):
        """ method to add a document to a index object
            or create a new object

            Parameters:
                key         -- the keyword to add to the index
                doc         -- the document id to add
                filename    -- the actual name of the document
        """
        key = key.lower()
        self.filenames[doc] = filename
        # see if we already have the word in the index
        docobj = None
        try:
            # get hash map entry for corresponding word
            docobj = self.index[key]
            try:
                # docobj should have tf and tf.idf entry
                docobj[doc]['tf'] += 1
                #tf.idf = tf * log (N / df)
                docobj[doc]['tf.idf'] = (float(docobj[doc]['tf'])
                                        * log(self.doc_count/len(self.index[key]),10))
            except KeyError:
                # enter a new document
                docobj[doc] = { 'tf' : 1, 'tf.idf' : 0}
                #tf.idf = tf * log (N / df)
                docobj[doc]['tf.idf'] = (float(docobj[doc]['tf'])
                                                  * log(self.doc_count/len(docobj),10))

        except KeyError:
            self.index[key] = { doc : { 'tf' : 1, 'tf.idf' : 0} }
            #tf.idf = tf * log (N / df)
            self.index[key][doc]['tf.idf'] = (float(self.index[key][doc]['tf'])
                                              * log(self.doc_count/len(self.index[key]),10))

    def get_documents(self,key):
        """ method to get documents which contain the given
            key

            Parameters:
                key -- the keyword to get the documents for

            Returns:
                array of document IDs for the given key
        """
        try:
            documents = self.index[key.lower()]
            return documents
        except Exception, e:
            return -1

    def get_intersected_list(self,keywords):
        """ method to get the intersected documents list for
            the keywords provided in the array

            Parameters:
                keywords -- array of keywords to search for

            Returns:
                intersected list of keywords
        """
        # list to start intersection with
        firstkeyword = keywords.pop(0)
        comparelist = self.get_documents(firstkeyword)
        lookuplist = self.get_documents(firstkeyword)
        if  (comparelist == -1):
            return -1
        # list to later hold the actual filenames
        returnlist = {}
        for key in keywords:
            docs = self.get_documents(key)
            if (docs == -1): return -1
            comparelist = filter(comparelist.has_key, docs.keys())
        for c in comparelist:
            # create hashmap with filename and score
            returnlist[self.filenames[c]] = c
        # fix to keep mutable keyword list consistent
        keywords.append(firstkeyword)
        return returnlist

    def get_andish_retrieval(self,keywords):
        """ method to do and-ish retrieval with scores

            Parameters:
                keywords -- array of keywords

            Returns:
                list of unioned search result, ordered by tf.idf score
        """
        # list for first keyword to start with
        ## get documents in the form of
        # { docname : score }
        resultlist = {}
        comparelist = {}

        for key in keywords:
            # get the rest of the gang
            docs = self.get_documents(key)
            if (docs == -1): continue
            for d in docs:
                name = self.filenames[d]
                if (resultlist.has_key(name)):
                    resultlist[name] += docs[d]['tf.idf']
                else:
                    resultlist[name] = docs[d]['tf.idf']

        sorted_results = sorted(resultlist.items(), key=itemgetter(1))
        sorted_results.reverse()
        return sorted_results


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

    def dump_objects(self,path):
        """ method to dump methods to disk

            Parameters:
                path -- filepath where to dump objects
        """
        self.parser.write_object_to_disk(path+"index.pickle",self.index)
        self.parser.write_object_to_disk(path+"filenames.pickle",self.filenames)

    def read_objects(self,path):
        """ method to read objects from disk

            Parameters:
                path -- filepath from where to read objects
        """
        self.index = self.parser.read_object_from_disk(path+"index.pickle")
        self.filenames = self.parser.read_object_from_disk(path+"filenames.pickle")
