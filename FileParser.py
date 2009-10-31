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
    def __init__(self,folder):
        """ Constructor

            Parameters:
                folder - path to the folder in which the documents to index reside
        """
        self.doccounter = 0
        self.documents = []
        self.folder = folder
        try:
            for root, folders, files in os.walk(self.folder):
                self.documents = files
        except:
            pass

    def parse_file(self,doc):
        """ Method to call for parsing a file

            Parameters:
                doc -- the filename of the document to parse

            Returns:
                hash of the textfile as ID
                array of words contained in the textfile
        """
        words = []
        try:
            f = open(self.folder+doc, 'r')
            for line in f.readlines():
                matches = re.findall('\w+', line)
                words.extend(matches)
            f.close()
        except:
            pass
        self.doccounter = self.doccounter+1
        return self.doccounter,words

    def get_documents(self):
        """ method to return documents"""
        return self.documents

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
