'''
Created on 19 במרס 2013

@author: Adam
'''
from gpsweb.models import Alert

class AlertChecker(object):
    '''
    given a location log entry, checks for any alerts that need to 'go off'.
    will call emailer and/or smser as needed.
    '''


    def __init__(self, LocationLog):
        '''
        Constructor
        '''
        self.locationLog = LocationLog
        
        
    def checkForAlarms(self):
        unit_alerts = Alert.object.filter(unit=self.locationLog.unit)
        speed_alerts    = [unit_alert for unit_alert in unit_alerts if unit_alert.alert_type == 'Speed']
        geofence_alerts = [unit_alert for unit_alert in unit_alerts if unit_alert.alert_type == 'Geofence']
        schedule_alerts = [unit_alert for unit_alert in unit_alerts if unit_alert.alert_type == 'Schedule']
        
        
#SPEED_ALERT = 1
#GEOFENCE_ALERT = 2
#SCHEDULE_ALERT = 3
    