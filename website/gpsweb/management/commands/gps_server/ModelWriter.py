import PacketParser
from gpsweb.models import Unit, LocationLog, Alert, AlertLog, Recipient
from datetime import datetime, timedelta
from emailer import mail 
from django.utils import timezone

def getUnitByImei(imei):
    unit = Unit.objects.filter(imei=imei)
    if unit: 
        unit = unit[0]
    else:
        unit = None
        
    return unit

def writeLocationLog(imei , data):
    #print "writeLocationLog"
    #print "imei=%s" % imei
    #print "data=%s" % data
    #print
    locationLog = LocationLog()

    utm = PacketParser.get_utm(data)
    locationLog.lat = utm[0]
    locationLog.long = utm[1]
    locationLog.timestamp = timezone.now()
    locationLog.speed = PacketParser.get_speed(data)
    locationLog.heading = PacketParser.get_heading(data)
    locationLog.unit = getUnitByImei(imei)
    
    locationLog.save() 
    
    checkAlerts(locationLog)
    
def resetAlertState(locationLog, alert):
    alert.state = locationLog.timestamp
    alert.save()
    
    
def checkAlerts(locationLog):
    alerts = Alert.objects.filter(unit=locationLog.unit)
    #print 'checkAlerts:'
    #print "locationLog = " + str(locationLog)
    for alert in alerts:
        if checkForTriggers(locationLog, alert):
            
            notification_sent = sendAlert(locationLog, alert)
            
            alertLog = AlertLog(location_log=locationLog,
                                alert=alert,
                                notification_sent=notification_sent)
            
            alertLog.save()
            
            if alertLog.notification_sent:
                resetAlertState(locationLog, alert)

def checkForTriggers(locationLog, alert):
    alert_exist = False
   
    if str(alert.type) == str(Alert.SPEED_ALERT):    
        if locationLog.speed >= alert.max_speed:
            alert_exist = True
            
    elif str(alert.type) == str(Alert.GEOFENCE_ALERT):
        if PacketParser.is_in_area(locationLog, alert):
            alert_exist = True
            
    elif str(alert.type) == str(Alert.SCHEDULE_ALERT):
        if PacketParser.is_in_time_slot(locationLog, alert):
            alert_exist = True
            
    return alert_exist

def getAlertFormat(alert, recipientType):
    if str(alert.type) == str(Alert.SPEED_ALERT):
        if recipientType == "email" : 
            return """<html> <head></head> <body> <p>Hi %(nickname)s!<br>  %(unit_name)s was going %(speed)s kph at <a href="https://maps.google.com/maps?q=%(location)s">click here to see the location!</a><br> </p> </body> </html>"""
        elif recipientType == "sms" :
            return ""
    if str(alert.type) == str(Alert.GEOFENCE_ALERT):
        if recipientType == "email" : 
            return ""
        elif recipientType == "sms" :
            return ""
    if str(alert.type) == str(Alert.SCHEDULE_ALERT):
        if recipientType == "email" : 
            return ""
        elif recipientType == "sms" :
            return ""

def sendAlert(locationLog, alert):
    if alert.state + timedelta(minutes = alert.cutoff) > locationLog.timestamp :
        return False
    recipients = getIterableRecipients(alert)
    
    for recipient in recipients:
        if recipient.email:
            sendMail(locationLog, alert, recipient)
        if recipient.telephone:
            #sendSMS(locationLog, alert, recipient)
            pass
    return True

def getIterableRecipients(alert):
    return alert.recipient.all()
    
    
def sendMail(locationLog, alert, recipient):
    mail_args = {    "nickname" : recipient.nickname, 
                     "unit_name" : locationLog.unit.name, 
                     "speed" : str(locationLog.speed), 
                     "location" : "%f%%20%f" % (locationLog.lat,locationLog.long),
                     "format" : getAlertFormat(alert,"email"),
                     "timestamp" : str(locationLog.timestamp),
                     "to" : str(recipient.email)}
    mail(mail_args)

