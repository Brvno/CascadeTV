import socket
import thread
import time
import AES


DNS_addr = ('192.168.1.72', 10000)
CIPHER_MODE = 1
BUFFER_SIZE = 30


class Viewer(object):
    def __init__(self, stream_name):
        self.stream_name = stream_name
        self.strSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.hide_str = False
        self.key = []
                
    def __init__(self):
        self.stream_name = False
        self.strSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.hide_str = False
        self.key = []
    
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
        if self.stream_name == False:
            self.stream_name = raw_input("Qual o nome da stream? ")
            a = raw_input("Possui alguma key? key_path / n ")
            if a != 'n':
                self.key = open(a,'r')
                self.hide_str = True
            

        ## Pegando IP do streamer escolhido
        stream_IP = self.retiraIP(stream_list,self.stream_name)
        stream_addr = (stream_IP, 9000)
        print stream_addr

        DNSSock.close()
        
        ##Avisando ao streamer que esta vivo
        ola = "Novo Viewer"
        if self.hide_str:
            ola = AES.encryptData(self.key, ola, CIPHER_MODE) 
        self.strSock.sendto(ola, stream_addr)
    
    ## para receber dados do server
    def receive(self):
        data = self.strSock.recvfrom(1024)
        if self.hide_str:
            data[0] = AES.decryptData(self.key, data[0], CIPHER_MODE)
        return data[0]


if __name__ == "__main__":
    eu = Viewer()
    eu.start()
    i = 0
    
    
    while True:
    
        # para cada imgem no buffer
    	for i in range(0,BUFFER_SIZE):
    	    # abre img
            fimg = open("./buffer/"+str(i)+".png", 'w')
            
            # pra cada Chunk
            while True:
                frame = eu.receive()
                if frame == "EOQ":
                    break
                fimg.write(data)
            fimg.close()
	
        

            
