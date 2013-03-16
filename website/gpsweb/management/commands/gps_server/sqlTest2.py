
import MySQLdb  
import gps_functions
from datetime import datetime  

                             
connection=MySQLdb.connect(host="127.0.0.1", user="amir", passwd="amir", db="gpstracker")  
cur=connection.cursor() 

imei = '863070011991451'
data = 'imei:863070011991451,ac alarm,1301160114,,F,171446.000,A,3205.4899,N,03447.3367,E,0.00,,;'
speed = gps_functions.get_speed(data)
heading = gps_functions.get_heading(data) #problem while null
utm = gps_functions.get_utm(data)
#Get unit id according to imei and add current location
cur.execute("SELECT unit_id FROM unit WHERE imei ="+str(imei))
unit_id = cur.fetchall()
unit_id = str(unit_id[0][0])
timestamp = datetime.now()
print "unit_id: "+unit_id
print "utm: "+str(utm)
print "speed: "+str(speed)
print "heading: "+str(heading) 
cur.execute("INSERT INTO `gpstracker`.`location_log` (`location_log_id`, `unit_id`, `timestamp`, `utm`, `speed`, `heading`) VALUES (NULL, '"+unit_id+"','"+str(timestamp)+"', GeomFromText('POINT("+str(utm[0]) +' '+ str(utm[1])+")',0), '"+str(speed)+"', '"+str(heading)+"');")
############

cur.close()
connection.close()


