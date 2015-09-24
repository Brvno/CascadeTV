import socket

a = raw_input("1 recv ou 2 send")

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if a == '1':
	img = open(raw_input("img name"), 'w')
	sock.bind(("", 10001))
	while True:
		data, addr = sock.recvfrom(512)
		if data == "EOQ":
			break
		img.write(data)
	img.close()
elif a == '2':
	img = open(raw_input("img name"), 'r')
	while True:
		st = img.readline(512)
		if not st:
			break
		sock.sendto(st,('localhost', 10001))
	img.close()
	sock.sendto('EOQ',('localhost', 10001))