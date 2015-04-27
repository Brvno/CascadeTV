__author__ = 'nautec'
# coding=utf-8
__author__ = 'Fischer'

import socket


#Classe para criação de Streamer nome do canal
#@parameters: name = nome do canal
class Viewer(object):
    def __init__(self, name, dns):
        self.name = name
        self.dns = dns


    #conecta DNS
    def conectarDNS(self):
        con_DNS = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        con_DNS.sendto("Viewer_name>>"+self.name, self.dns)
        print "Viewer_name>>"+self.name, self.dns
        data,data_address = con_DNS.recvfrom(1024)
        print data,data_address

    def requisita_stream(self, name):
        con_DNS.sendto("stream requirida>",self)
    def conectar_stream(self):
        pass


dns = ('172.16.1.59', 10000)
eu = Viewer("Fish", dns)
eu.conectarDNS()









