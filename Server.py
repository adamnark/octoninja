import socket
import signal
import sys
import MySQLdb 
import gps_functions
import sql_functions


def mysendall(clientsocket, data):
    clientsocket.sendall(data)
    print 'S: ' + data
   
def myrecv(clientsocket):
    data = clientsocket.recv(1024)
    print 'C: ' + data
    return data
    
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
    (clientsocket, address) = serversocket.accept() # start in a new thread ?
    print 'accepted connection from ' + str(address[0]) + ':' + str(address[1])

#    connection
    data = myrecv(clientsocket)
    imei = gps_functions.get_imei(data)
    answer = {"heartbeat":"ON", "init":"LOAD"}
    signal_types = ["tracker", "help me", "low battery"]
    count = 0;
    setup_repeat = False
    while count < 50:
        count += 1
        type = gps_functions.get_msg_type(data)
        if type in answer:
           mysendall(clientsocket,answer[type])
        elif type == "help me" or type == "low battery":
            mysendall(clientsocket,"**,imei:%s,E" % imei)
            # NOTIFY DB OR SOMETHING SOS
        if not setup_repeat:
            mysendall(clientsocket,'**,imei:' + imei +',C,20s')
            setup_repeat = True
        if type in signal_types:
            if gps_functions.is_valid_gps_signal(data):
                row = sql_functions.write_location_to_log(imei , data)
                sql_functions.check_alerts(row)
        data = myrecv(clientsocket)
    
    #    end connection

    print 'closing connection...'
    clientsocket.close()
    serversocket.close()

    raw_input("Press Enter to Exit")

main();