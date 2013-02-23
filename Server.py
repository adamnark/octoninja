import socket
import select
import Queue
import sys
import signal
import gps_functions
import sql_functions


class server:
    answer = {"heartbeat":"ON", "init":"LOAD"}
    signal_types = ["tracker", "help me", "low battery"]

    inputs = []
    outputs = []
    message_queue = {}
    setup_repeat = {}
    imei = {}

    serversocket = None
    
    def  __init__(self):
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.setblocking(0)
        self.mybind(self.serversocket)    
        
    def mysendall(self, clientsocket, data):
        clientsocket.sendall(data)
        print 'S: ' + data

    def queue_message(self, s, message):
        self.message_queue[s].put(message)
        if s not in self.outputs: 
            self.outputs.append(s)
       
    def myrecv(self, clientsocket):
        data = clientsocket.recv(1024)
        print 'C: ' + data
        return data

    def mybind(self, serversocket):
        print 'binding server...'
        try:
                self.serversocket.bind((socket.gethostname(), 9000))
        except socket.error, msg:
            print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()

    def cleanup_socket(self, s):
        #print 'closing connection with ' + s.getpeername()
        if s in self.outputs:
            self.outputs.remove(s)
        self.inputs.remove(s)
        try:
            del self.message_queue[s]
            del self.setup_repeat[s]
            del self.imei[s]
        except KeyError:
            print ' \b'
        finally:
            s.close()

    def signal_handler(self, signal, frame):
        print 'Ctrl+C was pressed, cleaning up'
        for s in self.inputs:
            cleanup_socket(s)
        raw_input("Press Enter to Exit")
        sys.exit()
    
    def start(self):
        print 'Press ctrl+c to escape'
        signal.signal(signal.SIGINT, server.signal_handler)

        self.serversocket.listen(5)
        self.inputs.append(self.serversocket)

        while self.inputs:
            readable, writable, exceptional = select.select(self.inputs, self.outputs, self.inputs)
            
            for s in readable:
                if s is self.serversocket:
                    # a readable server socket means we can accept
                    clientsocket, address = self.serversocket.accept()
                    print 'accepted connection from ' + str(address[0]) + ':' + str(address[1])
                    clientsocket.setblocking(0)
                    
                    self.inputs.append(clientsocket)
                    self.setup_repeat[clientsocket] = False
                    self.imei[clientsocket] = ''
                    self.message_queue[clientsocket] = Queue.Queue()
                    
                else: # s is an established connection, we can recv 
                    data = myrecv(s)
                    if data:
                        message_type = gps_functions.get_msg_type(data)

                        if message_type == 'init':
                            self.imei[s] = gps_functions.get_imei(data)

                        if message_type in self.answer:
                            self.queue_message(s, answer[message_type])
                        elif message_type == "help me" or message_type == "low battery": # SOS: SOMETHING HAPPEND TO A PERSON!
                            self.queue_message(s, "**,imei:%s,E" % self.imei[s])
                            
                        if not self.setup_repeat[s]:
                            self.setup_repeat[s] = True
                            self.queue_message(s, '**,imei:' + imei[s] +',C,20s')
                            
                        if message_type in self.signal_types:
                            if gps_functions.is_valid_gps_signal(data):
                                row = sql_functions.write_location_to_log(imei[s] , data)
                                sql_functions.check_alerts(row)
                                
                    else: # readable socket without data means the client disconnected 
                        self.cleanup_socket(s)
            
            for s in writable:
                try: 
                    next_msg = self.message_queue[s].get_nowait()
                except Queue.Empty:
                    print 'Queue.Empty exception: output queue for socket ' + s.getpeername() + ' is empty.'
                    self.outputs.remove(s)
                    
                else:
                    self.mysendall(s, next_msg)
            
            for s in exceptional:
                print  s.getpeername() + ' is in an exceptional state. cleaning up.'
                cleanup_socket(s)
 
def main():
    serv = server()
    serv.start()

 
if __name__=='__main__': 
    main()