"""
File: Server.py
Author: Daniel Schauenberg <schauend@informatik.uni-freiburg.de>
Description: class for implementing a search engine web server
"""
import socket
import time
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
                print "Client %s connected with port %s." % (itemgetter(0)(clientsock),itemgetter(1)(clientsock))
                while True:
                    data = connection.recv(8192)
                    if not data: break
                    #connection.sendall(data)
                    print data
                connection.close()
                print clientaddr
        finally:
            # don't leave socket open when going home
            self.socket.close()

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
