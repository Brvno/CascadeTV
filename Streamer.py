import socket
import threading
import time

DNS_IP = '192.168.1.72'
DNS_PORT = 10000
VIEWER_PORT = 9000 
CIPHER_MODE = 1


class Streamer(object):
        def __init__(self, name):
            # viewer list
            self.viewers_list = []

            # Viewers server
            self.viewSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            self.viewSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.stream_name = name

            # Hide Stream
            self.isHide = False
            self.key = []

        def listen_viewers(self):

            listen_addr = ("", VIEWER_PORT) 
            print listen_addr   
            self.viewSock.bind(listen_addr)
            
            while True:
                data, addr = self.viewSock.recvfrom(1024)
                # just viewers with the key can watch this stream
                if isHide:
                    data = decryptData(key, data, CIPHER_MODE)
                
                if data == "Novo Viewer":
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

        # Create Private Stream
        def hide(self, key = []):
            fkey = open(self.stream_name+".key","r+")
            if !key:
                key = AES.generateRandomKey(16)
                fkey.write(key)
            self.key = key\
            self.isHide = True

            
        def send_video(self, video):
            i=1;
            for viewer in self.viewers_list:
                print 'Transmitindo para: ', viewer,time.ctime()
                i+=1
                time.sleep(1)
                self.viewSock.sendto(video, viewer)

        def send(self, data):
            if isHide:
                data = AES.encryptData(key, data, CIPHER_MODE)

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
    os.system('clear')       
    minhaStream = Streamer(raw_input("Nome da Stream: "))
    opt = raw_input("Private? y/n")
    if opt == 'y':
        opt = raw_input("Ja tem uma key? KeyPath / n")
        if opt != 'n':
            fk = open(opt,r)
            minhaStream.hide(fk.read())
        else:
            minhaStream.hide()

    minhaStream.start()
        
    while True:
        minhaStream.send("yolo")
    
    
