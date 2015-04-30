import socket
import thread
import time

DNS_addr = ('192.168.1.13', 10000)

def retiraIP(lista, nome):
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



#requistar Stream
DNSSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
print 'Conectou no DNS'
DNSSock.sendto('viewer', DNS_addr)
stream_list, lixo = DNSSock.recvfrom(2048)
print 'Lista de Streamers'
print stream_list
stream_nome = raw_input("Qual o nome da stream? ")

## Pegando IP do streamer escolhido
stream_IP = retiraIP(stream_list, stream_nome)
stream_addr = (stream_IP, 9000)

print stream_addr

DNSSock.close()

##Avisando ao streamer que esta vivo 
strSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
strSock.sendto("hey", stream_addr)


#receive_video
i = 0
while True:
    video = strSock.recvfrom(1024)
    print i, ": " ,video[0], time.ctime()
    i += 1
    time.sleep(1)
    

        
