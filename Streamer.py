import socket
import threading
import time
DNS_IP = '192.168.1.13'

# viewer list
viewers_list = []

# Viewers server
viewSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
viewSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

def listen_viewers():

    listen_addr = ("", 9000) 
    print listen_addr   
    viewSock.bind(listen_addr)
    
    while True:
        data, addr = viewSock.recvfrom(1024)
        print "Novo Viewer: ", addr
        viewers_list.append(addr)
        
#avisa o dns que o streamer esta ativo
def send_dns(name):
    # DNS client socket
    DNSSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    dns_addr = (DNS_IP,10000)
    print "Conectou no DNS"
    DNSSock.sendto("stream:"+name, dns_addr)
    DNSSock.close()

def send_video(video):
    i=1;
    while True:

        for viewer in viewers_list:
            print 'Transmitindo para: ', viewer,time.ctime()
            i+=1
            time.sleep(1)
            viewSock.sendto(video, viewer)
        



stream_name = raw_input("Nome da Stream: ")
print 'Stream online ', stream_name
# Diz que esta online para o DNS
send_dns(stream_name )

# Esperar viewers e transmitir video
thread_listen = threading.Thread(target=listen_viewers)
thread_transmit = threading.Thread(target=send_video, args=(stream_name,))

thread_listen.start()
thread_transmit.start()
