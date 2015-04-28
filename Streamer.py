# coding=utf-8
__author__ = 'Brvno'

import socket
import sys
import thread

IP_DNS = '1.1.1'

# Classe para criacao de Streamer nome do canal
# @parameters: name = nome do canal
class Streamer(object):
    def __init__(self, name, dns):
        self.name = name
        self.dns = dns
        self.viewers_list = {}

        self.connect_dns()

        video = "Olha o Video"

        #Espera viewers enquanto envia o video para os ja conectados
        thread.start_new_thread(self.listen_viewer())
        thread.start_new_thread(self.send_video(video))


    #conecta DNS
    def connect_dns(self):
        con_DNS = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        con_DNS.sendto(self.name, self.dns)
        print "streamer_name>>"+self.name, self.dns
        con_DNS.close()

    #envia video para Client
    def send_video(self, video):
        while True:
            connection_viewers = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            for viewer in self.viewers_list:
                connection_viewers.sendto(video, viewer)


    def listen_viewer(self):
        #abre server
        connection = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        #connection.bind(self.dns)

        #conecta viewer
        while True:
        # Wait for a connection
             print >>sys.stderr, 'waiting for a connection'
             data, client_address = connection.recvfrom(1024)
             print "Connected", data, client_address
             self.viewers_list.append(client_address)




