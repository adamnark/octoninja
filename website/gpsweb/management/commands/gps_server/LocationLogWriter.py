from gpsweb.models import LocationLog ,Unit
from datetime import datetime  
import PacketParser
from AlertChecker import AlertChecker

class LocationLogWriter():
    def __init__(self, imei, data):
        self.imei = imei
        self.data = data
        
        
    def processRawData(self):   
        locationLog = self.makeNewLocationLog()
        alertChecker = AlertChecker(locationLog)
        alertChecker.checkForAlarms()
    
    def makeNewLocationLog(self):
        unit_collection = Unit.objects.get(imei=self.imei)
        if not unit_collection:
            print 'we got a message from unit we don\'t know, imei# %s, it said: "%s"' % self.imei, self.data  
            return
        unit = unit_collection[0] 
        car = unit.car
        utm =  PacketParser.get_utm(self.data)
        driver = car ? car.getDriverByDate(datetime.now()) : None
        
        kwargs = {  "timestamp" :  datetime.now(),
                    "lat" : utm[0],       
                    "long" : utm[1],      
                    "speed" : PacketParser.get_speed(self.data),
                    "heading" : PacketParser.get_heading(self.data)  ,               
                    "car" : car ,
                    "driver" : driver,
                  }

        logToWrite = LocationLog(**kwargs)
        logToWrite.save()
        return logToWrite
    