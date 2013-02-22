import socket
import select
import Queue
import sys
import signal
import gps_functions
import sql_functions

answer = {"heartbeat":"ON", "init":"LOAD"}
signal_types = ["tracker", "help me", "low battery"]

inputs = []
outputs = []
message_queue = {}
setup_repeat = {}
imei = {}


def mysendall(clientsocket, data):
    clientsocket.sendall(data)
    print 'S: ' + data

def queue_message(s, message):
    message_queue[s].put(message)
    if s not in outputs: outputs.append(s)
   
def myrecv(clientsocket):
    data = clientsocket.recv(1024)
    print 'C: ' + data
    return data

def mybind(serversocket):
    print 'binding server...'
    try:
            serversocket.bind((socket.gethostname(), 9000))
    except socket.error, msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()

def cleanup_socket(s):
    #print 'closing connection with ' + s.getpeername()
    if s in outputs:
        outputs.remove(s)
    inputs.remove(s)
    try:
        del message_queue[s]
        del setup_repeat[s]
        del imei[s]
    except KeyError:
        print ' \b'
    finally:
        s.close()

def signal_handler(signal, frame):
    print 'Ctrl+C was pressed, cleaning up'
    for s in inputs:
        cleanup_socket(s)
    raw_input("Press Enter to Exit")
    sys.exit()
    
def main():
    print 'Press ctrl+c to escape'
    signal.signal(signal.SIGINT, signal_handler)
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setblocking(0)
    mybind(serversocket)
    
    serversocket.listen(5)
    print 'listening!...'
    inputs.append(serversocket)

    while inputs:
        print "selectin'..."
        readable, writable, exceptional = select.select(inputs, outputs,inputs)
        #print '***inputs:***\n', inputs
        #print '***outputs:***\n', outputs
        
        for s in readable:
            if s is serversocket:
                # a readable server socket means we can accept
                clientsocket, address = serversocket.accept()
                print 'accepted connection from ' + str(address[0]) + ':' + str(address[1])
                clientsocket.setblocking(0)
                
                inputs.append(clientsocket)
                setup_repeat[clientsocket] = False
                imei[clientsocket] = ''
                message_queue[clientsocket] = Queue.Queue()
                
            else: # s is an established connection, we can recv 
                data = myrecv(s)
                if data:
                    message_type = gps_functions.get_msg_type(data)
                    #print s.getpeername(), " message_type = ", message_type 
                    
                    if message_type == 'init':
                        imei[s] = gps_functions.get_imei(data)

                    if message_type in answer:
                        queue_message(s, answer[message_type])
                    elif message_type == "help me" or message_type == "low battery": # NOTIFY DB OR SOMETHING SOS :: SOMETHING HAPPEND TO A PERSON
                        queue_message(s, "**,imei:%s,E" % imei[s])
                        
                    if not setup_repeat[s]:
                        queue_message(s, '**,imei:' + imei[s] +',C,20s')
                        setup_repeat[s] = True
                    if message_type in signal_types:
                        if gps_functions.is_valid_gps_signal(data):
                            row = sql_functions.write_location_to_log(imei[s] , data)
                            sql_functions.check_alerts(row)
                            
                else: # readable socket without data means the client disconnected 
                    cleanup_socket(s)
        
        for s in writable:
            try: 
                next_msg = message_queue[s].get_nowait()
            except Queue.Empty:
                print 'output queue for ', s.getpeername(), ' is empty'
                outputs.remove(s)
                
            else:
                mysendall(s, next_msg)
        
        for s in exceptional:
            print 'handling exceptional conditions for ', s.getpeername()
            cleanup_socket(s)
            
main()