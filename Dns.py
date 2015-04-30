import socket

# UDP server
UDPSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
UDPSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Listen on port 10000
# (to all IP addresses on this system)
listen_addr = ("",10000)
UDPSock.bind(listen_addr)

stream_lists = {}

# Report on all data packets received
# data -> <tipo>:<nome>
print 'CascadeTV DNS online'
while True:
        data, addr = UDPSock.recvfrom(1024)
        string = data.split(':')
        print string
        print data, addr
        print " --Stream List-- "
	print stream_lists
	#Se recebeu uma mensagem de uma stream,adiciona a stream na lista de todas as stream
        if string[0] == 'stream':
            stream_lists[string[1]] = addr
	#se recebeu uma mensagem de um viewer ele envia de volta uma lista com todas as streams e o ip dos streamers
        elif string[0] == 'viewer':
            UDPSock.sendto(str(stream_lists), addr)
            
