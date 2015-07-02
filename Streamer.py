import socket
import threading
import time

DNS_IP = '192.168.1.72'
DNS_PORT = 10000
VIEWER_PORT = 9000 

class Streamer(object):
        def __init__(self, name):
            # viewer list
            self.viewers_list = []

            # Viewers server
            self.viewSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            self.viewSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.stream_name = name

        def listen_viewers(self):

            listen_addr = ("", VIEWER_PORT) 
            print listen_addr   
            self.viewSock.bind(listen_addr)
            
            while True:
                data, addr = self.viewSock.recvfrom(1024)
                print "Novo Viewer: ", addr
                self.viewers_list.append(addr)
                
        #avisa o dns que o streamer esta ativo
        def send_dns(self, name):
            # DNS client socket
            DNSSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            dns_addr = (DNS_IP, DNS_PORT)
            print "Conectou no DNS"
            DNSSock.sendto("stream:"+name, dns_addr)
            DNSSock.close()


            
        def send_video(self, video):
            i=1;
            for viewer in self.viewers_list:
                print 'Transmitindo para: ', viewer,time.ctime()
                i+=1
                time.sleep(1)
                self.viewSock.sendto(video, viewer)

        def send(self, data):
            thread_transmit = threading.Thread(target=self.send_video, args=(data, ))            
            thread_transmit.start()
                            
        def start(self):

            print 'Stream online ', self.stream_name
            # Diz que esta online para o DNS
            self.send_dns(self.stream_name )

            # Esperar viewers
            thread_listen = threading.Thread(target=self.listen_viewers)
            thread_listen.start()



if __name__ == "__main__":            
    minhaStream = Streamer(raw_input("Nome da Stream: "))
    minhaStream.start()
        
    while True:
        minhaStream.send("yolo")
    
    
    
