# coding=utf-8
__author__ = 'Brvno'

import socket


#Classe para criação de Streamer nome do canal
#@parameters: name = nome do canal
class Streamer(object):
    def __init__(self, name, dns):
        self.name = name
        self.dns = dns


    #conecta DNS
    def conectarDNS(self):
        con_DNS = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        con_DNS.sendto("streamer_name>>"+self.name, self.dns)
        print "streamer_name>>"+self.name, self.dns

    #envia video para Client
    def sendVideo(self):
        pass

    def listenViewer(self):
        pass


dns = ('192.168.208.60', 10000)
eu = Streamer("Brvno", dns)
eu.conectarDNS()









