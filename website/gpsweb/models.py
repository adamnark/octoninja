from django.db import models
from django.contrib.auth.models import User

class Person(models.Model):
    owner   =   models.ForeignKey(User)
    nickname =  models.CharField(max_length=200)
    telephone = models.CharField(max_length=12)
    email =     models.EmailField()
    is_primary = models.BooleanField()
    def __unicode__(self):
        return self.nickname

class Driver(models.Model):
    person =     models.ForeignKey(Person)
    owner  =     models.ForeignKey(User)
    def __unicode__(self):
        return str(self.person)


class Car(models.Model):
    name =              models.CharField(max_length=200)
    car_number =        models.CharField(max_length=7) # 1234567 (which is 12-345-67)
    owner =             models.ForeignKey(User)
    primary_driver =    models.ForeignKey(Driver, blank=True, null=True, on_delete=models.SET_NULL)
    icon =              models.IntegerField()
    def __unicode__(self):
        return self.name
    def getDriverByDate(date):
        currDriver = self.primary_driver
        tempDrivers = TemporaryDriver.objects.filter(car = self).filter(start<date).filter(end>date)
        if tempDrivers:
            currDriver = tempDrivers[0]
        return currDriver
        

class Unit(models.Model):
    imei =      models.CharField(max_length=15)
    sim_num =   models.CharField(max_length=12)
    owner =     models.ForeignKey(User)
    car =       models.ForeignKey(Car, blank=True, null=True, on_delete=models.SET_NULL)
    def __unicode__(self):
        return self.imei

class TemporaryDriver(models.Model):
    driver =     models.ForeignKey(Driver)
    car =     models.ForeignKey(Car)
    start =     models.DateTimeField()
    end =     models.DateTimeField()
    def __unicode__(self):
        return self.name

class LocationLog(models.Model):
    timestamp = models.DateTimeField()
    lat =       models.CharField(max_length=13) # 34.7888233333
    long =      models.CharField(max_length=13) # 32.0915033333
    speed =     models.IntegerField()           # 101
    heading =   models.IntegerField()           # 216
    car =      models.ForeignKey(Car)
    def __unicode__(self):
        return "%s -- %s: (%s %s)" % (str(self.id), str(self.timestamp),str(self.lat),str(self.long))

class Alert(models.Model):
    name =      models.CharField(max_length=250)
    car =      models.ForeignKey(Car)
    state =     models.DateTimeField()
    cutoff =    models.IntegerField()
    recipients = models.ManyToManyField(Person)
    SPEED_ALERT = 1
    GEOFENCE_ALERT = 2
    SCHEDULE_ALERT = 3
    ALERTS_TYPE = (
        (SPEED_ALERT, 'Speed'),
        (GEOFENCE_ALERT, 'Geofence'),
        (SCHEDULE_ALERT, 'Schedule'))
    type =      models.IntegerField(max_length=1, choices=ALERTS_TYPE)
    max_speed = models.IntegerField()
    schedule_bit_field = models.CharField(max_length=168)
    geo_top_left_lat =       models.CharField(max_length=13) # 34.7888233333
    geo_top_left_long =      models.CharField(max_length=13) # 32.0915033333
    geo_bottom_right_lat =       models.CharField(max_length=13) # 34.7888233333
    geo_bottom_right_long =      models.CharField(max_length=13) # 32.0915033333

    def __unicode__(self):
        return "%s %s" % (self.car, self.name)

class AlertLog(models.Model):
    location_log = models.ForeignKey(LocationLog)
    alert = models.ForeignKey(Alert)
    notification_sent = models.BooleanField()
    marked_as_read = models.BooleanField()
    def __unicode__(self):
        sent = ' was sent' if self.notification_sent else ' was not sent'
        return self.alert.__unicode__() + sent
