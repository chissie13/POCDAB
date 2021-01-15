import socket
import time
import array

UDP_IP = "10.0.0.1" 	#IP to listen to
UDP_PORT = 4242		# port to listen to


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	#create a socket
sock.bind((UDP_IP, UDP_PORT))				#bind the socket to the IP and port
print("start")
cumData = ""
lrpn = -1 #lastReceivedPacketNumber
busy = False
list = []
megaList = []
packetCounter = 0
inTransmission = False

def checkChecksum(string, givenChecksum):
	string = string.encode()
	bytes = array.array('b', string)
	checksum = 0
	for i in range(len(bytes)):
		checksum ^= bytes[i]
	checksum = hex(checksum)
	print('checksum receiver: ' + checksum + '\n')
	if(checksum[2:] == givenChecksum):
		return True
	return False

def verifyFile(list, packetCounter):
	for x in range(packetCounter):
		if(list[x] == ''):
			print('file not complete, some packets went missing\n')
			return False
	return True

while True:
	data, addr = sock.recvfrom(4096)	#receive data
	data = data.decode('utf-8')
	packetNumber = int(data[0])
	packetCounter += 1
	data = data[1:]
	print('new Packet: ' + data + '\n')
	if(packetNumber == 0):
		inTransmission = True
		lrpn = -1
		if(list != []):
			megaList.append(list)
			list = []
		packetCounter = 0
		for x in megaList:
			if(data in x[0]):
				list = x
				megaList.remove(list)
	if(not inTransmission):
		continue
	if(packetNumber < lrpn):
		packetNumber += 9
	for x in range(packetNumber - (lrpn + 1)):
		list.append('')
		packetCounter += 1
	if(len(list) > packetCounter):
		list[packetCounter] = data
	else:
		list.append(data)
	if(packetNumber != 0 and '|' in data):
		if(verifyFile(list, packetCounter)):
			string = ''.join(list)
			fileData = string.split('|')
			string = fileData[0] + '|' + fileData[1]
			fileWithoutChecksum = string[:-2]
			checksum = string[-2:]
			if(checkChecksum(fileWithoutChecksum, checksum)):
				fileData = fileWithoutChecksum.split('|')
				f = open(fileData[0], 'w')
				f.write(fileData[1])
				f.close()
				print('file has been written\n')
				list = []
				inTransmission = False
			else:
				print('checksum was not equal')
	lrpn = packetNumber
