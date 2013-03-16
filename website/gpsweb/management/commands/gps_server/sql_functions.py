import MySQLdb.cursors
import gps_functions
from datetime import datetime, timedelta
from emailer import mail 
debug = True

def open_connection():
    sql_args = {"host":"127.0.0.1", 
            "user":"amir", 
            "passwd":"amir", 
            "db":"gpstracker"}
    connection = MySQLdb.connect(cursorclass=MySQLdb.cursors.DictCursor,**sql_args)  
    cur = connection.cursor()    
    return connection, cur

def write_location_to_log(imei , data):
    connection, cur = open_connection()
    
    row = {}
    row['imei'] = imei
    row['speed'] = gps_functions.get_speed(data)
    row['heading'] = gps_functions.get_heading(data)
    utm =  gps_functions.get_utm(data)
    row['utm_lat'] = utm[0]
    row['utm_long'] = utm[1]
    #Get unit id according to imei and add current locsation
    cur.execute("SELECT unit_id FROM unit WHERE imei ="+str(imei))
    unit_id = cur.fetchall()
    row['unit_id'] = str(unit_id[0]['unit_id'])
    row['timestamp'] = datetime.now()
    cur.execute("INSERT INTO `gpstracker`.`location_log` (`location_log_id`, `unit_id`, `timestamp`, `utm`, `speed`, `heading`) VALUES (NULL, '%(unit_id)s','%(timestamp)s', GeomFromText('POINT(%(utm_lat)s %(utm_long)s)',0), '%(speed)s', '%(heading)s');" % row)
    row['location_log_id'] = connection.insert_id() 
    cur.close()
    connection.close()
    return row

def check_alerts(row):
    alerts = get_all_alerts_of_device(row['imei'])
    connection, cur = open_connection()
    for alert in alerts:
        alert_exist = False
        msg_sent = 0
        if alert['type'] == 'speed':
            if int(row['speed']) >= int(alert['values']): #in speed alert value is speed limit
                msg_sent = send_alert(alert,row)
                alert_exist = True
        elif alert['type'] == 'geo-fence':
            if gps_functions.is_in_area(row['utm'],alert['values']):
                print "geo-fence sendAlert(alert,row)  !?!?!?!?!?!"
                alert_exist = True
        elif alert['type'] == 'schedule':
            if gps_functions.is_in_time_slot(row['timestamp'],alert['values']):
                print "schedule sendAlert()  !?!?!?!?!?!"
                alert_exist = True
        if alert_exist == True:
            q ="INSERT INTO  `gpstracker`.`alert_log` (`alert_id` ,`location_log_id` ,`notification_sent`) VALUES ('" + str(alert['alert_id']) + "', '" + str(row['location_log_id']) + "', '" + str(msg_sent)  + "')"
            print "q = " + q 
            cur.execute(q)
    cur.close()
    connection.close()        
def send_alert(alert,row):
    sent = 0
    if alert['state'] + timedelta(minutes = int(alert['cut_off'])) < row['timestamp']:
        connection, cur = open_connection()
        cur.execute("SELECT * FROM recipient JOIN alert_recipient WHERE alert_recipient.alert_id ="+ str(alert['alert_id']))
        recipients = cur.fetchall()
        # unit_name; 
        cur.execute("SELECT * FROM unit WHERE unit_id = " + str(row['unit_id']))
        unit_name = cur.fetchall()[0]['name']
        #format; 
        cur.execute("SELECT * FROM alert_format WHERE alert_format.type = '" + alert['type'] +"'")
        fmt = cur.fetchall()[0]['format']
        
        for recipient in recipients:
            if recipient['email'] != '':
                if debug == True: print 'send_alert: send email'
                mail_args = {"nickname":recipient['nickname'], 
                             "unit_name":str(unit_name), 
                             "speed":row['speed'], 
                             "location":str(row['utm_lat']) + "%20" + str(row['utm_long']),
                             "format": str(fmt),
                             "timestamp":row['timestamp'],
                             "to":recipient['email']}
                
                mail(mail_args)
                             
            if recipient['sms_number'] != '':
                print 'send_alert: send sms'
        cur.execute("UPDATE  `gpstracker`.`alert` SET  `state` =  '" + str(row['timestamp']) + "' WHERE `alert`.`alert_id` = '" + str(alert['alert_id']) + "';")
        cur.close()
        connection.close()
        sent = 1
        
    return sent

def get_all_alerts_of_device(imei):
    connection, cur = open_connection()
    cur.execute("SELECT unit_id FROM unit WHERE imei ="+str(imei))
    unit_id = cur.fetchall()
    unit_id = str(unit_id[0]['unit_id'])
    cur.execute("SELECT * FROM alert WHERE unit_id ="+ unit_id )
    alerts = cur.fetchall()
    cur.close()
    connection.close()
    return alerts
    
def get_last_alert_timestamp_from_type(alert_id):
    connection, cur = open_connection()
    cur.execute("SELECT timestamp FROM alert_log JOIN location_log WHERE alert_log.alert_id ="+ str(alert_id) +" AND alert_log.location_log_id = location_log.location_log_id")
    res = cur.fetchall()
    cur.close()
    connection.close()
    lst = []
    for t in res:
        lst.append(t['timestamp'])
    
    if len(lst) != 0:
        max_ = lst[0]
        for t in lst:
            max_ = t if max_ < t else max_
    else:
        max_ = None
       
    return max_
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
