import socket
import time
import array

UDP_IP = "10.0.0.1" 	#IP to listen to
UDP_PORT = 4242		# port to listen to


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	#create a socket
sock.bind((UDP_IP, UDP_PORT))				#bind the socket to the IP and port

print("start")

lrpn = -1 #lastReceivedPacketNumber

list = [] #list for current transmission
megaList = [] #list to store previous incomplete transmissions
packetCounter = 0 #counter for current transmission
inTransmission = False #is a file mid transmission?
'''
creates a checksum from the given string
checks if the checksum is the same as the given one
'''
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
'''
checks if there is an empty listvalue in the first [packetcounter]
amount of values in the list
'''
def verifyFile(list, packetCounter):
	for x in range(packetCounter):
		if(list[x] == ''):
			print('file not complete, some packets went missing\n')
			return False
	return True

while True: #keep receiving information
	data, addr = sock.recvfrom(4096)	#receive data
	data = data.decode('utf-8')
	packetNumber = int(data[0])		#packetnumber of the packet
	packetCounter += 1			#packetcounter of receive side
	data = data[1:]				#delete the packetnumber from the data
	print('new Packet: ' + data + '\n')
	if(packetNumber == 0):			#if packet is the first of the transmission
		inTransmission = True		#set transmission to true
		lrpn = -1			#set last received package number to -1 so package 0 is lrpn + 1
		if(list != []):			#if current transmission list is not empty
			megaList.append(list)	#store it in the transmission buffer
			list = []		#and reset the list
		packetCounter = 0		#reset the packetcounter for the new transmission
		for x in megaList:		#check if there is a list in the buffer that matches the new transmission
			if(data in x[0]):	#if it does go further with that list in the hopes of adding all previously lost data
				list = x
				megaList.remove(list)
	if(not inTransmission):			#if no package number 0 was received before this continue
		continue
	if(packetNumber < lrpn):		#package numbers run from 0-9 so after 9 it resets to 1, this so the next if works correctly
		packetNumber += 9
	for x in range(packetNumber - (lrpn + 1)): #if a package went missing add an empty value in the list
		list.append('')
		packetCounter += 1
	if(len(list) > packetCounter):		#if the listsize is bigger than the packetcounter (its a list from the buffer)
		list[packetCounter] = data	#replace the previously known data with the new one to hopefully add to previously lost data
	else:
		list.append(data)		#else just add the newly aquired data to the end of the list
	if((packetNumber != 0 and '|' in data) or data.count('|') == 2):	#if its the last package of the transmission
		if(verifyFile(list, packetCounter)):	#check if there is no empty data in the list
			string = ''.join(list)		#create string from the list
			fileData = string.split('|')	#get filedata (filename, filedata + checksum)
			string = fileData[0] + '|' + fileData[1]	#restore the string, with checksum
			fileWithoutChecksum = string[:-2]	#file to make the checksum on
			checksum = string[-2:]		#get checksum from the string
			if(checkChecksum(fileWithoutChecksum, checksum)):	#if the checksum is correct write the file
				fileData = fileWithoutChecksum.split('|')
				f = open(fileData[0], 'w')
				f.write(fileData[1])
				f.close()
				print('file has been written\n')
				list = []		#reset list
				inTransmission = False	#reset transmission
			else:
				print('checksum was not equal')
	lrpn = packetNumber	#set last received package number to the received package number
