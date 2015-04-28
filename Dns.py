import socket

# UDP server
UDPSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
UDPSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Listen on port 23456
# (to all IP addresses on this system)
listen_addr = ("",23491)
UDPSock.bind(listen_addr)

stream_lists = {}

# Report on all data packets received
# data -> <tipo>:<nome>
print 'Server online'
while True:
        data, addr = UDPSock.recvfrom(1024)
        string = data.split(':')
        print data, addr
        print stream_lists
        if string[0] == 'stream':
            stream_lists[string[1]] = addr
        elif string[0] == 'viewer':
            UDPSock.sendto(str(stream_lists), addr)
            
