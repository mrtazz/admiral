"""
File: Server.py
Author: Daniel Schauenberg <schauend@informatik.uni-freiburg.de>
Description: class for implementing a search engine web server
"""
import socket
import time
import re
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
        # actions which are executable by the webserver
        self.actions = {
                            "sentence" : self.repeat_sentence,
                            "default"  : self.http_404
                       }
        self.re_params = re.compile("\w+=\w+")
        self.re_action = re.compile("/\w+")
        # keyword to recognize that a sentence should be repeated
        self.sentence_keyword = "sentence"

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
                data = connection.recv(8192)
                if not data: break
                # build proper response for request
                response = self.get_header() + self.parse_header(data)
                connection.send(response)
                print data
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
        html = "\
                <html><head><title>Sentence repeated %s times</title></head>\
                <body> %s </body></html>\
                " % (count,rep_sent)
        return html

    def http_404(self,*args):
        """ basic HTTP 404 not found response

            Returns:
                http 404 html error page
        """
        html = "\
                <html>\
                <head><title>HTTP 404 error</title></head>\
                <body><h1>HTTP 404: File not found</h1></br>\
                <h4>Nothing to see here, tag along people.</h4>\
                </body>\
                </html>\
               "
        return html

    def get_header(self):
        """ method to create the basic header for returning to
            the client
        """
        http_ok_status = "HTTP/1.1 200 OK\n"
        date = time.strftime("%a, %d %b %Y %H:%M:%S %Z \n\n", time.gmtime())
        return http_ok_status + date

def main():
    foo = Webserver()
    foo.bind_to_port()


if __name__ == '__main__':
    main()
