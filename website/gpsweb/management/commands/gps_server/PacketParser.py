from django.utils.timezone import get_current_timezone ,get_current_timezone_name, make_naive
from gpsweb.utils import utils
from gpsweb.models import *

from pprint import pprint

def get_imei(data): 
    #only for A message
    msg_type = get_msg_type(data)
    if (msg_type == "tracker" or 
        msg_type == "low battery" or
        msg_type == "help me"):
        return data[5:20]
    elif (msg_type == "heartbeat"):
        return data
    elif (msg_type == "init"):
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
    splitData = data.split(',')
    if data[0:2] == "##":
        return "init"
    elif is_imei(data):
        return "heartbeat"
    elif splitData[1] in valid_types:
        return splitData[1]
    else:
        print 'get_msg_type: not valid message type'
        return None
        
def is_valid_gps_signal(data):
    spelt = data.split(',')
    return spelt[4] == 'F' #F=GPS signal \ L=no GPS signal

def get_speed(data):    
    data = data.split(',')
    num = data[11] if data[11] else '0.0' 
    return  int(float(num)*1.85200)
    
def get_heading(data):    
    data = data.split(',')
    if data[12] == '':
        return '0'
    else:
        return int(float(data[12]))

def get_utm(data):
    data = data.split(',')
    if data[3] == '@':
        lat = data[7]
        long = data[9]
    else:
        lat = get_utm_helper(data[7],data[8], 'S')
        long = get_utm_helper(data[9],data[10], 'W')
       
    return (lat, long)
    
def get_utm_helper(a, b, c):
    cord = float(a)
    num = float(int(cord)/100)
    num += ((cord - (num * 100)) /60)
    if b == c : num *= (-1)
    
    return num
    
def is_in_time_slot(timestamp,schedule):
    timestamp_naive = make_naive(timestamp,get_current_timezone())
    #weekday() Return the day of the week as an integer, where Monday is 0 and Sunday is 6
    weekDay = (timestamp_naive.weekday() + 1) % 7 
    hour = timestamp_naive.hour
    bit = (weekDay*24)+hour

    if schedule[bit] == '0':
        return True
    else:
        return False 


def is_out_of_area(locationLog, alert):
    ret = True
    lat, long = locationLog.lat, locationLog.long
    circles = AlertCircle.objects.filter(area=alert.geo_area)
    
    if alert.schedule_profile: #check area just if in 
        if not is_in_time_slot(locationLog.timestamp, alert.schedule_profile.schedule_bit_field):#don't check circles
            return False
            
    for circle in circles:
        if is_in_circle(circle, lat, long):
            ret = False
            break
    if not circles:
        ret = False
    
    
    return ret
    
def is_in_circle(circle, lat, long):
    dist_in_km = utils.calc_dist(lat, long, circle.center_lat, circle.center_long)
    dist = dist_in_km * 1000
    return dist <= circle.radius


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
    # print '~' * 15
    for packet in packets:
        print packet
        msg_type = get_msg_type(packet)
        # print "type = " + msg_type
        imei = get_imei(packet)
        print "imei = " + imei
        if msg_type in signal_types:
            if is_valid_gps_signal(packet):
                utm = get_utm(packet)
                # print "utm ", utm

if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
