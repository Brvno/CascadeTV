import socket
import sys
import thread

dns_address = ('172.16.1.59', 10000)


class Dns(object):

    def __init__(self):
        self.server_list = {}
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.connection.bind(dns_address)

        thread.start_new_thread(self.connect_viewer())
        thread.start_new_thread(self.connect_streamer())

    # search into dns list
    def search_stream(self, nome):
        if nome in self.server_list:
            return self.server_list[nome]
        else:
            return "not found"

    def connect_viewer(self):
        # Wait for a connection
        connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            print >>sys.stderr, 'waiting for a connection'
            data, client_address = connection.recvfrom(1024)
            print "Online:  "+"Viewer_name>>""+", data, client_address
            connection.sendto(self.server_list, client_address)

    def connect_streamer(self):
        while True:
        # Wait for a connection
            print >>sys.stderr, 'waiting for a connection'
            data, client_address = self.connection.recvfrom(1024)
            print "Online: streamer_name>>", "+", data, client_address
            self.server_list[data] = client_address
