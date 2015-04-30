import socket

class DnsServer(object):
    def __init__(self):
        # UDP server
        self.UDPSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)    
        self.UDPSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Listen on port 10000
        # (to all IP addresses on this system)
        self.listen_addr = ("",10000)
        self.stream_lists = {}


    #envia a lista das streams para os viewers
    def send_list(self, addr):
        self.selfUDPSock.sendto(str(self.stream_lists), addr)

    #comeca DNS Server
    def start(self):
        self.UDPSock.bind(self.listen_addr)
        while True:
            data, addr = self.UDPSock.recvfrom(1024)
            string = data.split(':')
            print string
            print data, addr
            print " --Stream List-- "
            print self.stream_lists
            # Report on all data packets received
            # data -> <tipo>:<nome>

            #Se recebeu uma mensagem de uma stream,adiciona a stream na lista de todas as stream
            if string[0] == 'stream':
                self.stream_lists[string[1]] = addr
            #se recebeu uma mensagem de um viewer ele envia de volta uma lista com todas as streams e o ip dos streamers
            elif string[0] == 'viewer':
                self.send_list(addr) 
            
    



print 'CascadeTV DNS online'

CascadeTvDns = DnsServer()
CascadeTvDns.start()

    
            
