#!/usr/bin/env python
"""
File: admiral.py
Author: Daniel Schauenberg <schauend@informatik.uni-freiburg.de>
Description: usage script to invoke webserver with indexed documents
"""
import sys
import Server

from optparse import OptionParser

def main():
    """ main function to initialize the whole web server
    """
    # initialize parser
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-f", "--folder", action="store", dest="folder",metavar="FOLDER",
                      help="folder where the documents for indexing reside")
    parser.add_option("-p", "--port", action="store", type="int", dest="port", metavar="NUM", default="3366",
                      help="port on which the server should listen")
    parser.add_option("-d", "--docroot", action="store", dest="docroot", metavar="DOCROOT", default=".",
                      help="docroot for pages to be served from the webserver")

    (options, args) = parser.parse_args()

    if not options.folder:
        parser.error("No folder to parse provided.")
    else:
        print "Creating server object."
        server = Server.Webserver(port=options.port, docroot=options.docroot)
        print "Indexing Files..."
        size = server.build_index(options.folder)
        print "Index created with %s words." % (size)
        print "Binding server to port ... done."
        server.bind_to_port()

if __name__ == '__main__':
    main()
