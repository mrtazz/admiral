## 
# @file Search.py
# @brief client for inverted index searching
# @author Daniel Schauenberg <schauend@informatik.uni-freiburg.de>
# @version 0.1
# @date 2009-10-25

import InvertedIndex
import FileParser
from operator import itemgetter

def main():
    maindir = "/Users/mrtazz/Documents/Computer Science/rfc_2000/"
    foo = InvertedIndex.IndexManager()
    bar = FileParser.DocumentParser(maindir)
    files = bar.get_folder_content()
    filelookup = {}
    #print "Add words."
    for f in files:
        h,words = bar.parse_file(maindir+f)
        filelookup[h] = f
        for w in words:
             foo.add_key(str(w),h)

    # dump objects
    foo.write_object_to_disk(obj=filelookup,filepath="/Users/mrtazz/Documents/Computer Science/rfc_names")
    foo.write_object_to_disk(filepath="/Users/mrtazz/Documents/Computer Science/rfc_searchindex")

    # load objects
    #foo.read_object_from_disk(filepath="/Users/mrtazz/Documents/Computer Science/rfc_searchindex")
    #filelookup = foo.read_object_from_disk(ret=True,filepath="/Users/mrtazz/Documents/Computer Science/rfc_names")

    print foo.get_index_size()
    #csv = open("/Users/mrtazz/Documents/Computer Science/freq.csv",'w')
    #wfreq = foo.get_word_frequencies()
    #freq = 0;
    #count = 0;
    #for f in wfreq:
        #   if (f[1] == freq):
            #   count += 1
            #else:
                #s = "%s,%s\n" % (freq,count)
                #csv.write(s)
                #count = 1
                #freq = f[1]

    #print "Searching"
    searchwords = ['affeaffe', 'rfc']
    l =  foo.get_intersected_list(searchwords)
    #print "Size of the index is %s." % (foo.get_index_size())
    for i in l:
        print filelookup[i]

if __name__ == '__main__':
    main()
