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

        con_DNS.sendto(self.name, self.dns)
        print "streamer_name>>"+self.name, self.dns

    #envia video para Client
    def sendVideo(self):
        pass

    def listenViewer(self):
        #abre server
        self.conexao = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.endereco_dns = ('172.16.1.59',9000)
        self.conexao.bind(self.endereco_dns)
        #conecta viewer
        while True:
        # Wait for a connection
             print >>sys.stderr, 'waiting for a connection'
             data, client_address = self.conexao.recvfrom(1024)
             print "conectou", data, client_address


dns = ('172.16.1.59', 10000)
eu = Streamer("FishFIshg", dns)
eu.conectarDNS()









