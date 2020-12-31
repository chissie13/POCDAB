import socket
import time

UDP_IP = "10.0.0.1"
UDP_PORT = 4242

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
print("start")
cumData = ""
while True:
	data, addr = sock.recvfrom(4096)
	cumData += data
	print("Received data: " + cumData)
	if(cumData.count('|') >= 2):
		cumData = cumData[:-1]
		fileData = cumData.split('|')
		filename = fileData[0]
		file = fileData[1]
		print(filename)
		print(file)
		f = open(filename, 'a')
		f.write(file)
		f.close()
		cumData = ''

