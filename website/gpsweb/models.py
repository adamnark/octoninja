from django.db import models
from django.contrib.auth.models import User


class Unit(models.Model):
    name =      models.CharField(max_length=200)
    imei =      models.CharField(max_length=15)
    sim_num =   models.CharField(max_length=12)
    owner =     models.ForeignKey(User)
    icon =      models.IntegerField()
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

class Alert(models.Model):
    unit =      models.ForeignKey(Unit)
    state =     models.DateTimeField()
    cutoff =    models.IntegerField()
    recipient = models.ManyToManyField(Recipient)
    SPEED_ALERT = 1
    GEOFENCE_ALERT = 2
    SCHEDULE_ALERT = 3
    ALERTS_TYPE = (
        (SPEED_ALERT, 'Speed'),
        (GEOFENCE_ALERT, 'Geofence'),
        (SCHEDULE_ALERT, 'Schedule'))
    type =      models.CharField(max_length=1, choices=ALERTS_TYPE)
    max_speed = models.IntegerField()
    schedule_bit_field = models.CharField(max_length=168)
    geo_top_left_lat =       models.CharField(max_length=13) # 34.7888233333
    geo_top_left_long =      models.CharField(max_length=13) # 32.0915033333
    geo_bottom_right_lat =       models.CharField(max_length=13) # 34.7888233333
    geo_bottom_right_long =      models.CharField(max_length=13) # 32.0915033333
    def __unicode__(self):
        return self.unit.__unicode__()
      


class AlertLog(models.Model):
    location_log = models.ForeignKey(LocationLog)
    alert = models.ForeignKey(Alert)
    notification_sent = models.BooleanField()
    def __unicode__(self):
        sent = 'sent' if self.notification_sent else 'not sent'
        return self.alert.__unicode__() + sent
