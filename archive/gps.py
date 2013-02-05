import socket
import signal
import sys

def mysendall(clientsocket, data):
    clientsocket.sendall(data)
    print 'S: ' + data
   
def myrecv(clientsocket):
    data = clientsocket.recv(1024)
    print 'C: ' + data
    return data
	
def get_imei(data):
	return data[8:23]

def main():
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print 'binding server...'
	try:
			serversocket.bind((socket.gethostname(), 9000))
	except socket.error , msg:
		print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()
	serversocket.listen(5)
	print 'listening!...'
	(clientsocket, address) = serversocket.accept()
	print 'accepted connection from ' + str(address[0]) + ':' + str(address[1])

#	"""   connection      """
	data = myrecv(clientsocket)
	imei = get_imei(data)

	mysendall(clientsocket,'LOAD')
	data = myrecv(clientsocket)

	count = 0;
	while (count < 100000):
		count = count + 1
		print "====" + str(count) + "====" 
		data = myrecv(clientsocket)
		if (data == (imei + ';')):
			mysendall(clientsocket,'ON')
		elif (count == 1):
			mysendall(clientsocket,'**,imei:' + imei +',C,20s')

#	"""   end connection  """

	print 'closing connection...'
	clientsocket.close()
	serversocket.close()

	raw_input("Press Enter to Exit")

main();