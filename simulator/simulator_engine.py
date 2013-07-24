import re
import socket
import random
import time
import sys

SLEEP_INTERVAL = 1
PORT = 9000

imei_pool = [ x * 15 for x in '123456789']


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
        print 'starting connection...'
        self.connect()
        print 'sending handshake...'
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
        print "Done sending as %s" % self.imei
        self.socket.close()
        sys.exit(0)
            
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

        
def main():
    filename = sys.argv[1]
    imei = int(sys.argv[2])
    sim = Simulator(filename, imei)
    sim.start()
    
if __name__ == '__main__': 
    main()
