import socket
import time

UDP_IP = "10.0.0.1" 	#IP to listen to
UDP_PORT = 4242		# port to listen to


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	#create a socket
sock.bind((UDP_IP, UDP_PORT))				#bind the socket to the IP and port
print("start")
cumData = ""
lrpn = -1 #lastReceivedPacketNumber

def reset():
	print('reset has been called')
	lrpn = -1
	cumData = ""

while True:
	data, addr = sock.recvfrom(4096)	#receive data
	data = data.decode('utf-8')
	packetNumber = int(data[0])
	if(packetNumber - 1 != lrpn):
		reset()
		print('Packet lost, reseting...')
		if(packetNumber != 0):
			continue
	data = data[1:]
	cumData += data				#gather the data and make one long string out of it
	print("Received data: " + data + '\n')
	lrpn += 1
	if(lrpn > 9):
		lrpn = 0
	if(cumData.count('|') >= 2):		#if the string contains 2 or more special tokens
		cumData = cumData[:-1]		#get the filename and data and write it to the file
		fileData = cumData.split('|')
		filename = fileData[0]
		file = fileData[1]
		print("saved new file:")
		print(filename + '\n')
		f = open(filename, 'w')
		f.write(file)
		f.close()
		reset()
