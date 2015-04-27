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
        self.endereco_dns = ('172.16.1.59',10000)
        self.conexao.bind(self.endereco_dns)

    def procura_stream(self,nome):
        if nome in self.dic:
            return self.dic[nome]
        else:
            return "deu merda"
    def conecta_viewer(self):
        #self.conexao.listen(1)
        while True:
        # Wait for a connection
             print >>sys.stderr, 'waiting for a connection'
             data, client_address = self.conexao.recvfrom(1024)
             print "conectou  "+"Viewer_name>>""+", data, client_address
             self.conexao.sendto()

    def conecta_streamer(self):
        #self.conexao.listen(1)
        asd = True
        while asd:
        # Wait for a connection
             print >>sys.stderr, 'waiting for a connection'
             data, client_address = self.conexao.recvfrom(1024)
             print "conectou  "+"streamer_name>>""+", data, client_address
             self.dic[data] = client_address
             #print self.dic
             asd = False
Unico = Dns()

Unico.inicia_server()
Unico.conecta_streamer()
Unico.conecta_viewer()




