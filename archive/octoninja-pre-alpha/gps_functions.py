import socket
import signal
import sys
import MySQLdb 
            
def get_imei(data):#only for A message
    type = get_msg_type(data)
    if (type == "tracker" or 
        type == "low battery" or
        type == "help me"):
        return data[5:20]
    elif (type == "heartbeat"):
        return data
    elif (type == "init"):
        return data[8:23]
    
def is_imei(data):
    if (len(data) == 16): # imei+;
        for c in data[:-1]:
            if (not str.isdigit(c)):
                return False
        return True
    return False

def parse(packet):
	packet = packet.split(',')
	return packet    
    
def get_msg_type(data):
    valid_types = ["tracker","low battery","help me"]
    spelt = data.split(',')
    if data[0:2] == "##":
        return "init"
    elif is_imei(data):
        return "heartbeat"
    elif spelt[1] in valid_types:
        return spelt[1]
    else:
        print 'get_msg_type: not valid message type'
        return None
        
def is_valid_gps_signal(data):
    spelt = data.split(',')
    return spelt[4] == 'F' #F=GPS signal \ L=no GPS signal

def get_speed(data):    
    data = data.split(',')
    return  int(float(data[11])*1.85200)
    
def get_heading(data):    
    data = data.split(',')
    if data[12] == '':
        return '0'
    else:
        return data[12]

def get_utm(data):
    data = data.split(',')
    lat = get_utm_helper(data[7],data[8], 'S')
    long = get_utm_helper(data[9],data[10], 'W')
       
    return (lat, long)
    
def get_utm_helper(a, b, c):
    cord = float(a)
    num = float(int(cord)/100)
    num += ((cord - (num * 100)) /60)
    if b == c : num *= (-1)
    
    return num
    

def is_in_time_slot(timestamp,value):
    print ('*'*10) + ' gps_functions.is_in_time_slot() not implemented! ' + ('*'*10)

def is_in_area(utm,value):
    print ('*'*10) + ' gps_functions.is_in_area() not implemented! ' + ('*'*10)
    

def main():
    """
    just for unit testing
    """
    signal_types = ["tracker", "help me", "low battery"]
    packets = [#"012345678912345",
            #"##,imei:012345678912345,A;",
            #"imei:012345678912345,help me,000000000,13554900601,L,;",
            #"imei:012345678912345,help me,0809231429,13554900601,F,062947.294,A,2234.4026,N,11354.3277,E,0.00,;",
            #"imei:012345678912345,low battery,000000000,13554900601,L,;",
            "imei:012345678912345,low battery,0809231429,13554900601,F,062947.294,A,2234.4026,N,11354.3277,E,0.00,;",
            #"imei:012345678912345,tracker,0809231929,13554900601,F,112909.397,A,2234.4669,N,11354.3287,E,0.11,;",
            "imei:012345678912345,tracker,000000000,13554900601,L,;",
            "imei:863070011991451,tracker,1301111556,,F,075604.000,A,3205.4805,N,03447.3385,E,0.00,,;863070011991451;"]

    print 'analyzing %s packets:' % str(len(packets))
    print '~' * 15
    for packet in packets:
        print packet
        type = get_msg_type(packet)
        print "type = " + type
        imei = get_imei(packet)
        print "imei = " + imei
        if type in signal_types:
            if is_valid_gps_signal(packet):
                utm = get_utm(packet)
                print "utm ", utm
        print '*' * 15

if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
