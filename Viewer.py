import socket
import thread
import time
DNS_PORT = 10000
DNS_addr = ('192.168.1.72', DNS_PORT)
VIEWER_PORT = 9000


class Viewer(object):
    def __init__(self, stream_name):
        self.stream_name = stream_name
        self.strSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    def __init__(self):
        self.stream_name = ''
        self.strSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    #extrai ip de uma lista de dado um nome
    def retiraIP(self, lista, nome):
        aux = lista.split(',')
        pos = -1
        i = 0
        for k in aux:
            pos = k.find(nome)
            i +=1
            if(pos != -1):
	            break

        ip = aux[i-1].split('(')
        
        return ip[1].replace("'", "")
        
    
    #iniciar o o viewer
    def start(self):
        #requistar Stream
        DNSSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print 'Conectou no DNS'
        DNSSock.sendto('viewer', DNS_addr)
        stream_list, lixo = DNSSock.recvfrom(2048)
        print 'Lista de Streamers'
        print stream_list
        
        while True:

            self.stream_name = raw_input("Qual o nome da stream? ")

            if self.stream_name in stream_list:  
                ## Pegando IP do streamer escolhido
                stream_IP = self.retiraIP(stream_list,self.stream_name)
                stream_addr = (stream_IP, 9000)
                print stream_addr
                break
            else:
                print "Nao tem feijao"

        DNSSock.close()
        
        ##Avisando ao streamer que esta vivo 
        self.strSock.sendto("hey", stream_addr)
    
    ## para receber dados do server
    def receive(self):
        data = self.strSock.recvfrom(1024)
        return data[0]


if __name__ == "__main__":
    eu = Viewer()
    eu.start()
    i = 0
    while True:
        video = eu.receive()
        print i, ": " ,video, time.ctime()
        i += 1
        time.sleep(1)
        

            
