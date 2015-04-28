import socket
import thread

DNS_addr = ('192.168.208.25', 23491)

#requistar Stream
DNSSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
print 'Conectou no DNS: '
DNSSock.sendto('viewer', DNS_addr)
stream_list = DNSSock.recvfrom(2048)
print stream_list

#TODO: Escolher canal da lista e retirar a tupla IP,Port e colocar na stream_addr
stream_addr = ('IP', 'port')

DNSSock.close()

strSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
strSock.sendto("hey", stream_addr)


#receive_video


while True:
    video = strSock.rcvfrom(1024)


        
