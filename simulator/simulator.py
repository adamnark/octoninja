import re
import socket
import random
import time

SLEEP_INTERVAL = 3
PORT = 9900

imei_pool = [
	'863070011991452',
	'863070011991453',
	'863070011991454',
	]

class Simulator():
	def __init__(self, pathToGarminXML, imei_num):
		self.route = []
		self.loadXML(pathToGarminXML)
		self.imei = imei_pool[imei_num]
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def loadXML(self, pathToGarminXML):
		lines = open(pathToGarminXML).readlines()
		for line in lines:
			pattern = '<gpxx:rpt lat="([\.\d]+)" lon="([\.\d]+)"/>'
			for match in re.findall(pattern, line):
				self.route.append(match)		

	def start(self):
		print 'start connection'
		self.connect()
		print 'send handshake'
		handshake = '##,imei:%s,A;' % self.imei
		self.send(handshake)
		self.recv()
		print 'for each route point, send a data packet:'
		for point in self.route:
			speed = self.generateSpeed()
			message = 'imei:%s,tracker,1301020247,@,F,184712.000,A,%s,N,%s,E,%s,0.00,;' % (self.imei, point[0], point[1], speed)
			print '> ' + message
			self.send(message)
			time.sleep(SLEEP_INTERVAL)
			
	def generateSpeed(self):
		a = random.randint(0, 80)
		a = str(a)
		a += '.00'
		return a
	
	def connect(self):
		self.socket.connect(('192.168.1.17', PORT))
	
	def send(self, message):
		if self.socket:
			self.socket.sendall(message)

		
	def recv(self):
		d = self.socket.recv(1024)
		if not d:
			print 'connection closed by server'

		
import sys
def main():
	if len(sys.argv) == 2:
		sim = Simulator(sys.argv[0],sys.argv[1])
		sim.start()
	
if __name__ == '__main__': 
	main()
