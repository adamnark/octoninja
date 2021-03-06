import socket, select, Queue, sys
from signal import signal
import PacketParser
import ModelWriter


class Server:
    
    def  __init__(self, port=9000):
        self.answer = {"heartbeat":"ON", "init":"LOAD"}
        self.signal_types = ["tracker", "help me", "low battery"]

        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.inputs = []
        self.outputs = []
        self.message_queues = {}
        self.setup_repeat = {}
        self.IMEIs = {}
        
        self.serversocket.setblocking(0)
        self.mybind(port)    
        self.serversocket.listen(5)
        self.inputs.append(self.serversocket)
        
    def mysendall(self, clientsocket, data):
        try:
            clientsocket.sendall(data)
        except(socket.error):
            self.cleanup_socket(clientsocket)    
        else:
            print '>>> ' + data

    def queue_message(self, s, message):
        self.message_queues[s].put(message)
        if s not in self.outputs: 
            self.outputs.append(s)
       
    def myrecv(self, clientsocket):
        try:
            data = clientsocket.recv(1024)
        except(socket.error):
            self.cleanup_socket(clientsocket)
        else:
            print '<<< ' + data
            return data

    def mybind(self, port):
        print 'binding server on %s...' % port
        try:
            self.serversocket.bind((socket.gethostname(), port))
        except socket.error, msg:
            print 'Bind failed. Error Code : ' + str(msg[0]) + ' - ' + msg[1]
            sys.exit()

    def cleanup_socket(self, s):
        #print 'closing connection with ' + s.getpeername()
        if s in self.outputs:
            self.outputs.remove(s)
        if s in self.inputs:
            self.inputs.remove(s)
        self.message_queues.pop(s, 0)
        self.setup_repeat.pop(s, 0)
        self.IMEIs.pop(s, 0)
        s.close()

    def signalHandler(self, signal, frame):
        print 'Ctrl+C was pressed, cleaning up'
        for s in self.inputs:
            self.cleanup_socket(s)
        raw_input("Press Enter to Exit")
        sys.exit()
    
    def acceptConnection(self):
        clientsocket, address = self.serversocket.accept()
        print 'accepted connection from ' + str(address[0]) + ':' + str(address[1])
        clientsocket.setblocking(0)
        
        self.inputs.append(clientsocket)
        self.setup_repeat[clientsocket] = False
        self.IMEIs[clientsocket] = ''
        self.message_queues[clientsocket] = Queue.Queue()
        
    def recvFromClientSocket(self, clientSocket):
        data = self.myrecv(clientSocket)
        if data:
            message_type = PacketParser.get_msg_type(data) # "tracker","low battery","help me", "heartbeat", "init"

            if message_type == 'init':
                self.IMEIs[clientSocket] = PacketParser.get_imei(data)

            if message_type in self.answer:
                self.queue_message(clientSocket, self.answer[message_type])
                
            elif message_type == "help me" or message_type == "low battery": 
                self.queue_message(clientSocket, "**,IMEIs:%s,E" % self.IMEIs[clientSocket])
                # we should do something else, perhaps add database log.
                
            if not self.setup_repeat[clientSocket]:
                self.queue_message(clientSocket, '**,IMEIs:' + self.IMEIs[clientSocket] +',C,20s')
                self.setup_repeat[clientSocket] = True
                
            if message_type in self.signal_types:
                if PacketParser.is_valid_gps_signal(data):
                    #try:
                    ModelWriter.writeLocationLog(self.IMEIs[clientSocket],data)
                    #except:
                    #    print 'Error writing to Location Log'
                else: 
                    print 'recvFromClientSocket: not valid gps signal \r\n imei=%s\r\ndata=%s' % (self.IMEIs[clientSocket],data)
        else: 
            # readable socket without data means the client disconnected
            self.cleanup_socket(clientSocket)
        
    def writeMessageFromSocketQueue(self, writeableSocket):
        try: 
            next_msg = self.message_queues[writeableSocket].get_nowait()
        except Queue.Empty:
            print 'Queue.Empty exception: output queue for socket ' , writeableSocket.getpeername() , ' is empty. Removing socket from writeable queue.'
        else:
            self.mysendall(writeableSocket, next_msg)
        finally:
            if writeableSocket in self.outputs:
                self.outputs.remove(writeableSocket)
                        
   
    def handleExceptionalSocket(self, exceptionalSocket):
        print  exceptionalSocket.getpeername(), ' is in an exceptional state. cleaning up.'
        self.cleanup_socket(exceptionalSocket)
       
    def start(self):
        print 'starting server ...'
        while self.inputs:
            readable, writable, exceptional = select.select(self.inputs, self.outputs, self.inputs)
            
            for s in readable:
                if s is self.serversocket:
                    # a readable server socket means we can accept
                    self.acceptConnection()
                    
                else: # s is an established connection, we can recv 
                    self.recvFromClientSocket(s)
                                
            for s in writable:
                self.writeMessageFromSocketQueue(s)
            
            for s in exceptional:
                self.handleExceptionalSocket(s)

