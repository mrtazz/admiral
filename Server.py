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

            Parameters:
                host -- address to listen on, default is all
                port -- port to listen on
        """
        self.host = host
        self.port = port
        self.socket = None
        self.index_manager = None
        # actions which are executable by the webserver
        self.actions = {
                            "sentence" : self.repeat_sentence,
                            "search"   : self.search_words,
                            "index"    : self.search_index_page,
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
        # build inverted index object
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
        # get the first line of the header
        data = data.split("\n")[0]
        # HEAD request gets special treatment (returns immediately)
        if (re.findall("^HEAD",data)):
            return self.get_header(code=200)
        action = None
        try:
            # get the url to determine the method to call
            action = str(re.findall(self.re_action,data)[0])
            action = re.sub("\/","",action)
            action = re.sub("\?","",action)
        except:
            pass
        # build a dict from all the GET parameters for easier
        # handling later on
        params = {}
        matches = re.findall(self.re_params,data)
        for m in matches:
            params[m.split("=")[0]] = m.split("=")[1]
        # call the appropriate method from the actions hashmap
        return self.actions.get(action,self.http_404)(params)


    def repeat_sentence(self,params):
        """ method to repeat a specific sentence a provided
            number of times

            Parameters:
                count -- number of times to repeat the sentence
        """
        try:
            # set the count to the number given in the URL
            count = int(params["repeat"])
        except:
            count = 1
        rep_sent = ""
        # produce the sentence the desired amount of times
        for i in range(0,count):
            rep_sent += "All your base are belong to us! </br>"
        title = "Sentence repeated %s times" % count
        html = self.get_html_page(title,rep_sent)
        return self.get_header(code = 200,length = len(html)) + html

    def search_words(self,params):
        """ method to search for keywords in the inverted index

            Parameters:
                params -- the URL GET parameters

            Return:
                all documents containing the search words
        """
        # see if we got keywords provided
        try:
            keywords = params["keywords"].split("+")
        except:
            html = self.get_html_page("not found","<h2>No keywords given.</h2>")
            return self.get_header(code = 200,length = len(html)) + html

        # the first word is saved, because later on we have to put it
        # on the list again since it is a mutable python object and we
        # would lose one keyword for the intersection otherwise
        first_word = keywords.pop(0)
        keywords_text = "" + first_word

        # append all keywords to a string
        for k in keywords:
            keywords_text += " "+k
        # append the first item again
        keywords.append(first_word)

        # basic page definitions
        title = "Search Results"
        body = '<h2>Inverted Index Search:</h2> \
                <form name="input" action="/search" method="get">\
                Insert words to search for: </br>\
                <input type="text" name="keywords" value="%s" />\
                <input type="submit" value="Submit" />\
                </form> <h1> Search results: </h1>' % (keywords_text)

        # get the list intersection for the keywords
        result = self.index_manager.get_andish_retrieval(keywords)

        # check if there were any results
        if (result == -1):
            # result -1 means one of the keywords wasn't in the index
            body += '<h3> The keyword combination \"%s\" was not found in\
                    any document.</h3>' % (keywords_text)
        else:
            # put together documents containing the keywords
            body +=  '<h3> Search result for keywords \"%s\": </h3>' % (keywords_text)
            # add all the results to the page
            for r in result:
                body += "%s   ||  Score: %s.</br>" %(r[0],r[1])

        html = self.get_html_page(title,body)
        return self.get_header(code = 200,length = len(html)) + html

    def search_index_page(self,params):
        """ simple method to display a page with a search box

            Parameters:
                params -- HTTP GET parameters

            Returns:
                html index page
        """
        # html form for entering search terms
        title = "Inverted Index Search"
        body = '<h2>Inverted Index Search:</h2>\
                <form name="input" action="/search" method="get">\
                Insert words to search for: </br>\
                <input type="text" name="keywords" />\
                <input type="submit" value="Submit" /></form>'
        html = self.get_html_page(title,body)
        return self.get_header(code = 200,length = len(html)) + html

    def http_404(self,*args):
        """ basic HTTP 404 not found response

            Returns:
                http 404 html error page
        """
        # build a nice 404 page
        title = "HTTP 404 error"
        body = "<h1>HTTP 404: File not found</h1></br>\
                <h4>Nothing to see here, tag along people.</h4>"
        html = self.get_html_page(title,body)
        return self.get_header(code = 404,length = len(html)) + html

    def get_header(self, code=200, length=""):
        """ method to create the basic header for returning to
            the client
        """
        # build header according to given code
        status = {
                     200 : "HTTP/1.1 200 OK\n",
                     404 : "HTTP/1.1 404 Not Found\n"
                 }
        content = "Content-Type: text/html; charset=UTF-8\n"
        date = "Date: %s" % (time.strftime("%a, %d %b %Y %H:%M:%S %Z \n", time.localtime()))
        server = "Server: py-admiral 0.1 \n"
        length = "Content-Length: %s \n" % (length)
        return status[code] + content + date + server + length + "\n"

    def get_html_page(self,title,content):
        """ method to return a basic html header with a title

            Parameters:
                title   -- the html page title
                content -- the content of the page

            Returns:
                a basic html page
        """
        html =  "<html>\
                <head><title>%s</title></head>\
                <body>%s</body></html>" % (title,content)
        return html
