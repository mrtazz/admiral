"""
File: Server.py
Author: Daniel Schauenberg <schauend@informatik.uni-freiburg.de>
Description: class for implementing a search engine web server
"""
import socket
import time
import re
import InvertedIndex
from operator import itemgetter

class Webserver:
    """ class for implementing a web server, serving the
        inverted index search engine to the outside
        (or inside) world
    """
    def __init__(self, host='', port=3366):
        """ constructor method to set the webserver basic settings
        """
        self.host = host
        self.port = port
        self.socket = None
        self.index_manager = None
        # actions which are executable by the webserver
        self.actions = {
                            "sentence" : self.repeat_sentence,
                            "search"   : self.search_words,
                            "default"  : self.http_404
                       }
        self.re_params = re.compile("\w+=[a-zA-Z0-9+]+")
        self.re_action = re.compile("/\w+")
        # keyword to recognize that a sentence should be repeated
        self.sentence_keyword = "sentence"

    def build_index(self,filepath):
        """ method to build the inverted index from which the
            searches will be done later on

            Parameters:
                filepath -- the path to the folder to index
        """
        self.index_manager = InvertedIndex.IndexManager(filepath)
        self.index_manager.build_index()
        return self.index_manager.get_index_size()

    def bind_to_port(self):
        """ simple method to make the port binding easier
        """
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.bind((self.host,self.port))
        # number of queued connections
        self.socket.listen(3)
        # create endless loop waiting for connections
        # can be interrupted via CTRL-C
        try:
            while True:
                # get socket object and client address
                connection, clientsock = self.socket.accept()
                print "Client %s connected." % (itemgetter(0)(clientsock))
                data = connection.recv(4096)
                if not data: break
                # build proper response for request
                response = self.parse_header(data)
                connection.send(response)
                connection.close()
                print "Client %s disconnected." % (itemgetter(0)(clientsock))
        finally:
            # don't leave socket open when going home
            self.socket.close()

    def parse_header(self,data):
        """ method to parse the HTTP header for specific actions

            Parameters:
                data -- the header data to be parsed

            Return:
                the proper response to the request
        """
        data = data.split("\n")[0]
        if (re.findall("^HEAD",data)):
            return self.get_header(code=200)
        action = None
        try:
            action = str(re.findall(self.re_action,data)[0])
            action = re.sub("\/","",action)
            action = re.sub("\?","",action)
        except:
            pass
        params = {}
        matches = re.findall(self.re_params,data)
        for m in matches:
            params[m.split("=")[0]] = m.split("=")[1]
        return self.actions.get(action,self.http_404)(params)


    def repeat_sentence(self,params):
        """ method to repeat a specific sentence a provided
            number of times

            Parameters:
                count -- number of times to repeat the sentence
        """
        try:
            count = int(params["repeat"])
        except:
            count = 1
        rep_sent = ""
        for i in range(0,count):
            rep_sent += "All your base are belong to us! </br>"
        html = "<html><head><title>Sentence repeated %s times</title></head>\
                <body> %s </body></html>\
                " % (count,rep_sent)
        return self.get_header(code=200,length=len(html))+html

    def search_words(self,params):
        """ method to search for keywords in the inverted index

            Parameters:
                params -- the URL GET parameters

            Return:
                all documents containing the search words
        """
        # start of html output
        html = "<html><head><title>Search Results</title></head>\
                <body><h1> Search results: </h1>"
        print params
        try:
            keywords = params["keywords"].split("+")
        except:
            html = "<html><head><title>not found</title></head>\
                    <body><h2>No keywords given.</h2></body></html>"
            return self.get_header(code=200,length=len(html))+html
        keys = keywords
        # the first word is saved, because later on we have to put it
        # on the list again since it is a mutable python object and we
        # would lose one keyword for the intersection otherwise
        first_word = keys.pop(0)
        keywords_text = ""+first_word
        # append all keywords to a string
        for k in keys:
            keywords_text += ", "+k
        keywords.append(first_word)
        print keywords
        # get the list intersection for the keywords
        result = self.index_manager.get_intersected_list(keywords)
        # check if there were any results
        if (result == -1):
            # result -1 means one of the keywords wasn't in the index
            html+= "<h3> The keyword combination %s was not found in\
                    any document.</h3>" % (keywords_text)
        else:
            # put together documents containing the keywords
            html +="<h3> The keywords %s appear together in these\
                    documents: </h3>" % (keywords_text)
            for r in result:
                html += r+"</br>"

        html += "</body></html>"
        return self.get_header(code=200,length=len(html))+html

    def http_404(self,*args):
        """ basic HTTP 404 not found response

            Returns:
                http 404 html error page
        """
        html = "<html>\
                <head><title>HTTP 404 error</title></head>\
                <body><h1>HTTP 404: File not found</h1></br>\
                <h4>Nothing to see here, tag along people.</h4>\
                </body>\
                </html>\
               "
        return self.get_header(code=404,length=len(html))+html

    def get_header(self, code=200, length=""):
        """ method to create the basic header for returning to
            the client
        """
        status = {
                     200 : "HTTP/1.1 200 OK\n",
                     404 : "HTTP/1.1 404 Not Found\n"
                 }
        content = "Content-Type: text/html; charset=UTF-8\n"
        date = "Date: %s" % (time.strftime("%a, %d %b %Y %H:%M:%S %Z \n", time.localtime()))
        server = "Server: py-admiral 0.1 \n"
        length = "Content-Length: %s \n" % (length)
        return status[code] + content + date + server + length + "\n"
