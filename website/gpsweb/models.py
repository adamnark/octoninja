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
    def __unicode__(self):
        return self.name

class LocationLog(models.Model):
    timestamp = models.DateTimeField()
    lat =       models.CharField(max_length=13) # 34.7888233333
    long =      models.CharField(max_length=13) # 32.0915033333
    speed =     models.IntegerField()           # 101
    heading =   models.IntegerField()           # 216
    unit =      models.ForeignKey(Unit)
    def __unicode__(self):
        return str(self.timestamp) + ': (' +  self.lat + ' ' + self.long + ')'

class Recipient(models.Model):
    telephone = models.CharField(max_length=12)
    email =     models.EmailField()
    nickname =  models.CharField(max_length=200)
    def __unicode__(self):
        return self.nickname

class AbstractAlert(models.Model):
    unit =      models.ForeignKey(Unit)
    state =     models.DateTimeField()
    cutoff =    models.IntegerField()
    recipient = models.ManyToManyField(Recipient)
    def __unicode__(self):
        return self.unit.__unicode__()

class SpeedAlert(AbstractAlert):
    max_speed = models.IntegerField()
    def __unicode__(self):
        return super(SpeedAlert, self).__unicode__() + ' @ ' + str(self.max_speed) + ' kph'

class AlertLog(models.Model):
    location_log = models.ForeignKey(LocationLog)
    alert = models.ForeignKey(AbstractAlert)
    notification_sent = models.BooleanField()
    def __unicode__(self):
        sent = 'sent' if self.notification_sent else 'not sent'
        return alert.__unicode__() + sent
