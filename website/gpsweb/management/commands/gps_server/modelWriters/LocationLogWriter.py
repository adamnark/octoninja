'''
Created on Mar 17, 2013

@author: Amir
'''

from gpsweb.models import LocationLog ,Unit
from datetime import datetime  
import PacketParser

class LocationLogWriter():
    def __init__(self, imei, data):
        self.imei = imei
        self.data = data
        
        
    def processRawData(self):   
        locationLog = self.makeNewLocationLog()
        ##### make a new alert checker, and give it locationLog!
        
    
    def makeNewLocationLog(self):
        unit_collection = Unit.objects.get(imei=self.imei)
        if not unit_collection:
            print 'we got a message from unit #%s, it said: "%s"' % self.imei, self.data  
            return
        unit = unit_collection[0] 
        utm =  PacketParser.get_utm(self.data)
        kwargs = {  "timestamp" :  datetime.now(),
                    "lat" : utm[0],       
                    "long" : utm[1],      
                    "speed" : PacketParser.get_speed(self.data),
                    "heading" : PacketParser.get_heading(self.data)  ,               
                    "unit" : unit ,               
                  }

        logToWrite = LocationLog(**kwargs)
        logToWrite.save()
        return logToWrite