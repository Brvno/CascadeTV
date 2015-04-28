# coding=utf-8
__author__ = 'Fischer'

import socket
import random


#Classe para criação de Streamer nome do canal
#@parameters: name = nome do canal
class Viewer(object):
    def __init__(self, name, dns):
        self.name = name
        self.dns = dns

        #conecta DNS
        con_DNS = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        con_DNS.sendto("Viewer_name>>"+self.name, self.dns)
        print "Viewer_name>>"+self.name, self.dns
        server_list, data_address = con_DNS.recvfrom(1024)
        print server_list

        #stream escolhida
        self.stream_name = random.choice(server_list)
        self.stream_address = server_list[self.stream_name]


        #connect stream
        self.connection_stream = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.connection_stream.sendto(self.name, self.stream_address)

        print("Watching: ", self.stream_name)

        while True:
            self.stream = self.connection_stream.recvfrom(1024)
            print self.stream


dns = ('172.16.1.59', 10000)
eu = Viewer("Fish", dns)
eu.conectarDNS()









