import socket
import threading

DNS_IP = '192.168.208.25'

# viewer list
viewers_list = []

# Viewers server
viewSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
viewSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

def listen_viewers():

    listen_addr = ("", 9876)    
    viewSock.bind(listen_addr)
    
    while True:
        data, addr = viewSock.recvfrom(1024)
        print "Novo Viewer: ", addr
        viewers.append(addr)
        

def send_dns(name):
    # DNS client socket
    DNSSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    dns_addr = (DNS_IP,23491)
    print "Conectou no DNS"
    DNSSock.sendto("stream:"+name, dns_addr)
    DNSSock.close()

def send_video(video):
    while True:
        for viewer in viewers_list:
            print 'Transmitindo para: ', viewer
            viewSock.sendto(video, viewer)
        


print 'Stream online'
# Diz que esta online para o DNS
send_dns("Brvno")

# Esperar viewers e transmitir video
thread_listen = threading.Thread(target=listen_viewers)
thread_transmit = threading.Thread(target=send_video, args=("Yaargh",))

thread_listen.start()
thread_transmit.start()
