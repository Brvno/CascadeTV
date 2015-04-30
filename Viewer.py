import socket
import thread

DNS_addr = ('192.168.201.33', 10000)

#requistar Stream
DNSSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
print 'Conectou no DNS: '
DNSSock.sendto('viewer', DNS_addr)
stream_list = DNSSock.recvfrom(2048)
print stream_list
print "escolha a stream (0,1,2,3...)"

#retira o ip e a porta da string
string =  str(stream_list[0])
string = string.split(',')
print
print string[1]
print
string2 = string[1]
print string2.split(')')
print
porta = string2.split(')')
porta = porta[0]
print porta
print
print string [0]
string3 = string[0].split('(')
print
print string3[1]
print
IP =string3[1]
IP = IP[1:15]
print IP
print
por = int (porta)
#TODO: Escolher canal da lista e retirar a tupla IP,Port e colocar na stream_addr
stream_addr = (IP,9000)
print stream_addr
print
DNSSock.close()

strSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
strSock.sendto("hey", stream_addr)


#receive_video


while True:
    video = strSock.recvfrom(1024)
    print video[0]

        
