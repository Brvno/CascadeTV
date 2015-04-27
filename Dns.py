__author__ = 'aluno'
import socket
import sys
class Dns(object):

    def __init__(self,):
       self.dic = {}
    def adiciona_stream(self,nome,ip):
        self.dic[nome] = ip

    def inicia_server(self):
        self.conexao = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.endereco_dns = ('192.168.208.60',10000)
        self.conexao.bind(self.endereco_dns)

    def procura_stream(self,nome):
        if nome in self.dic:
            return self.dic[nome]
        else:
            return "deu merda"
    def conecta_viewer(self,ip_viewer,porta_viewer):
        pass

    def conecta_streamer(self):
        #self.conexao.listen(1)
        while True:
        # Wait for a connection
             print >>sys.stderr, 'waiting for a connection'
             data, client_address = self.conexao.recvfrom(1024)
             print "conectou", data, client_address
Unico = Dns()

Unico.inicia_server()
Unico.conecta_streamer()





