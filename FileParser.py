"""
# @file FileParser.py
# @brief class to parse the documents
# @author Daniel Schauenberg <schauend@informatik.uni-freiburg.de>
# @version 0.1
# @date 2009-10-25

"""

import sys
import os
import hashlib
import re
import pickle

class DocumentParser:
    """ Document parsing class
    """
    documents = []
    def __init__(self,folder):
        """ Constructor

            Parameters:
                folder - path to the folder in which the documents to index reside
        """
        try:
            for root, folders, files in os.walk(folder):
                self.documents = files
        except:
            pass

    def get_words_from_file(self, filename):
        """ method to get all words from a textfile

            Parameters:
                filename -- file to parse
            Returns:
                array of words contained in the file
        """
        words =[]
        try:
            f = open(filename, 'r')
            for line in f.readlines():
                line = re.sub(r'\W+', ' ', line)
                words.extend(line.split(None))
            f.close()
        except:
            pass
        return words

    def parse_file(self, filename):
        """ Method to call for parsing a file

            Parameters:
                filename -- name of the textfile to parse

            Returns:
                hash of the textfile as ID
                array of words contained in the textfile
        """
        try:
            f = open(filename,'r')
            h = hashlib.sha1(f.read())
            f.close()
        except:
            pass
        words = self.get_words_from_file(filename)
        return h.hexdigest(),words

    def get_folder_content(self):
        """ method to return the list of files in the specified folder

            Returns:
                array of documents returned from os.walk()
        """
        return self.documents

    def write_index_to_disk(self,filepath):
        """ method to write the index to the provided filepath

            Parameters:
                filepath -- file to write the index to
        """
        try:
            f = open(filepath, 'w')
            pickle.dump(self.index, f)
        except:
            pass

    def read_index_from_disk(self,filepath):
        """ method to read index from file

            Parameters:
                filepath -- file to read index from
        """
        try:
            f = open(filepath, 'r')
            self.index = pickle.load(f)
        except:
            pass
