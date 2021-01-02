import socket
import time

UDP_IP = "10.0.0.1" 	#IP to listen to
UDP_PORT = 4242		# port to listen to

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	#create a socket
sock.bind((UDP_IP, UDP_PORT))				#bind the socket to the IP and port
print("start")
cumData = ""
while True:
	data, addr = sock.recvfrom(4096)	#receive data
	cumData += data				#gather the data and make one long string out of it
	print("Received data: " + data)
	if(cumData.count('|') >= 2):		#if the string contains 2 or more special tokens
		cumData = cumData[:-1]		#get the filename and data and write it to the file
		fileData = cumData.split('|')
		filename = fileData[0]
		file = fileData[1]
		print("saved new file:")
		print(filename)
		print(file)
		f = open(filename, 'w')
		f.write(file)
		f.close()
		cumData = ''			#reset string for next document

