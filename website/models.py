from django.db import models
from django.contrib.auth.models import User

#-#################-#
#     OLD TABLES    # 
#-#################-#
# alert_format      #  
# alert_log         #
# alert             #
# alert_recipient   #
# recipient         #
# location_log      #
# unit              #
# unit_owner        #
# user              #
#-#################-#

class Unit(models.Model):
    name =      models.CharField(max_length=200)
    imei =      models.CharField(max_length=15)
    sim_num =   models.CharField(max_length=12)
    owner =     models.ForeignKey(User)

class LocationLog(models.Model):
    timestamp = models.DateTimeField()          # !WE SHOULD WRITE TO THE DATABASE A DATETIME OBJECT WHEN INSERTING SO THIS WORKS TOGETHER!
    long =      models.CharField(max_length=13) # 32.0915033333
    lat =       models.CharField(max_length=13) # 34.7888233333
    speed =     models.IntegerField()           # 101
    heading =   models.IntegerField()           # 216
    unit =      models.ForeignKey(Unit)

class Recipient(models.Model):
    telephone = models.CharField(max_length=12)
    email =     models.EmailField()
    nickname =  models.CharField(max_length=200)

class AbstractAlert(models.Model):
    unit =      models.ForeignKey(Unit)
    state =     models.DateTimeField()
    cutoff =    models.IntegerField()
    format =    models.CharField(max_length=2000)
    recipient = models.ManyToManyField(Recipient)
    def get_format(): #abstact method!
        raise NotImplementedError("AbstractAlert.get_format(): you need to override this method!")

class SpeedAlert(AbstractAlert):
    max_speed = models.IntegerField()
    def get_format(self):
        return r'<html><head></head><body><p>Hi %(nickname)s!<br>  %(unit_name)s was going %(speed)s kph at <a href="https://maps.google.com/maps?q=%(location)s">click here to see the location!</a><br></p></body></html>' 

class AlertLog():
    location_log = models.ForeignKey(LocationLog)
    alert = models.ForeignKey(AbstractAlert)
    notification_sent = models.BooleanField()
