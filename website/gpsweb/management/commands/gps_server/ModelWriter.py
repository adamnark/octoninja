import PacketParser
from gpsweb.models import *
from datetime import datetime, timedelta
from emailer import mail
from django.utils import timezone
from Smser import sms
def getCarByImei(imei):
    unit = Unit.objects.filter(imei=imei)
    if unit:
        unit = unit[0]
        car = unit.car
    else:
        car = None

    return car

def writeLocationLog(imei , data):

    locationLog = LocationLog()

    utm = PacketParser.get_utm(data)
    locationLog.lat = utm[0]
    locationLog.long = utm[1]
    locationLog.timestamp = timezone.now()
    locationLog.speed = PacketParser.get_speed(data)
    locationLog.heading = PacketParser.get_heading(data)
    locationLog.car = getCarByImei(imei)
    locationLog.driver = locationLog.car.getDriverByDate(locationLog.timestamp)

    print "writeLocationLog"
    print "lat=%s" % locationLog.lat
    print "long=%s" % locationLog.long
    print

    locationLog.save()

    checkAlerts(locationLog)

def resetAlertState(locationLog, alert):
    alert.state = locationLog.timestamp
    alert.save()

def checkAlerts(locationLog):
    alerts = Alert.objects.filter(car=locationLog.car)
    for alert in alerts:
        if checkForTriggers(locationLog, alert):
            processTriggerdAlert(locationLog, alert)

def processTriggerdAlert(locationLog, alert):
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

    if str(alert.type) == str(Alert.GEOFENCE_ALERT):
        if PacketParser.is_out_of_area(locationLog, alert):
            alert_exist = True

    if str(alert.type) == str(Alert.SCHEDULE_ALERT):
        if PacketParser.is_in_time_slot(locationLog.timestamp, alert.schedule_profile.schedule_bit_field):
            alert_exist = True

    print "checkForTriggers returned " + str(alert_exist)
            
    return alert_exist

def getAlertFormat(alert, recipientType):
    preface = "Hi %(nickname)s!"
    google_maps_url = "https://maps.google.com/maps?q=%(location)s"
    html_pface = "<html><head></head><body><p>" + preface + "</p><h4>" + alert.name + " alert has gone off!</h4> "
    link = "<a href='"+google_maps_url+"'>Click here to see the location!</a>"

    if str(alert.type) == str(Alert.SPEED_ALERT):
        if recipientType == "email" :
            return html_pface + "<p>%(driver_name)s was going %(speed)s kph with %(car_name)s. " + link + "<br></p></body></html>"
        elif recipientType == "sms" :
            return "%(driver_name)s was going %(speed)s kph with %(car_name)s. \nLocation: " + google_maps_url
    if str(alert.type) == str(Alert.GEOFENCE_ALERT):
        if recipientType == "email" :
            return html_pface + "<p>%(driver_name)s is moving with %(car_name)s outside of the permitted perimeter. " + link + " <br></p></body></html>"
        elif recipientType == "sms" :
            return "%(driver_name)s is moving with %(car_name)s outside of permitted perimeter. \nLocation: " + google_maps_url
    if str(alert.type) == str(Alert.SCHEDULE_ALERT):
        if recipientType == "email" :
            return html_pface + "<p>%(driver_name)s is moving with %(car_name)s outside of the permitted hours. " + link + "<br></p></body></html>"
        elif recipientType == "sms" :
            return "%(driver_name)s is moving with %(car_name)s outside permitted hours. \nLocation: " + google_maps_url

def sendAlert(locationLog, alert):
    if alert.state + timedelta(minutes = alert.cutoff) > locationLog.timestamp :
        return False
    recipients = getIterableRecipients(alert)

    for recipient in recipients:
        if recipient.email:
            sendMail(locationLog, alert, recipient)
        if recipient.telephone:
            sendSms(locationLog, alert, recipient)
            pass
    return True

def getIterableRecipients(alert):
    return alert.recipients.all()

def sendMail(locationLog, alert, recipient):
    mail_args = {    "nickname" : recipient.nickname,
                     "driver_name" : locationLog.driver,
                     "car_name" : locationLog.car,
                     "speed" : str(locationLog.speed),
                     "location" : "%s%%20%s" % (locationLog.lat,locationLog.long),
                     "format" : getAlertFormat(alert,"email"),
                     "timestamp" : str(locationLog.timestamp),
                     "to" : str(recipient.email)}
    mail(mail_args)

def sendSms(locationLog, alert, recipient):
    sms_args = {     "nickname" : recipient.nickname,
                     "driver_name" : locationLog.driver,
                     "car_name" : locationLog.car,
                     "speed" : str(locationLog.speed),
                     "location" : "%s%%20%s" % (locationLog.lat,locationLog.long),
                     "format" : getAlertFormat(alert,"sms"),
                     "timestamp" : str(locationLog.timestamp),}

    telephone = recipient.telephone
    message = sms_args['format'] % sms_args
    try:
        sms(telephone, message)
    except:
        print "couldn't send sms"

