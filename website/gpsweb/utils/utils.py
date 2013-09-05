from math import sin, cos, radians, degrees, acos
from gpsweb.models import *
import datetime
def calc_dist(lat_a, long_a, lat_b, long_b):
    if (lat_a == lat_b) and (long_a == long_b):
        return 0
    lat_a = float(lat_a)
    long_a = float(long_a)
    lat_b = float(lat_b)
    long_b = float(long_b)
    
    lat_a = radians(lat_a)
    lat_b = radians(lat_b)
    delta_long = radians(long_a - long_b)
    cos_x = (
        sin(lat_a) * sin(lat_b) +
        cos(lat_a) * cos(lat_b) * cos(delta_long)
        )
    multiplier = 6371 # for kilometers
    #multiplier = 3959 # for miles

    return acos(cos_x) * multiplier
 

  
    
class RouteDetails:    
    def __init__(self, locationList):
        self.locationList = locationList
        self.length = self.routeLengthFunc
        self.avgSpeed = self.avgSpeedFunc
        self.maxSpeed = self.maxSpeedFunc
		
    def routeLengthFunc(self):
        dist = 0
        if not self.locationList:
            return dist
            
        prevLat = self.locationList[0].lat
        prevLong = self.locationList[0].long
        for curr_location in self.locationList:
            dist += calc_dist(  prevLat,
                                prevLong,
                                curr_location.lat,
                                curr_location.long)
            prevLat = curr_location.lat
            prevLong = curr_location.long
        return round(dist, 3)
        
    def avgSpeedFunc(self):
        sum = 0
        if not self.locationList:
            return 0
        for curr_location in self.locationList:
            sum += curr_location.speed
        return int(round(sum / len(self.locationList) , 0))
        
    def maxSpeedFunc(self):
        if not self.locationList:
            return 0
        max = 0 
        for curr_location in self.locationList:
            if curr_location.speed > max:
                max = curr_location.speed
        return max        
        
class CarPrimaryDriver:
    def __init__(self, car, driver):
        self.car = car
        self.driver= driver 
def userCarDrivers(user):
    carDrivers = []
    cars = Car.objects.filter(owner_id=user.id)
    for car in cars:
        driver = car.getPrimaryDriver()
        val = CarPrimaryDriver(car, driver)
        carDrivers.append(val)
    return carDrivers 

class CarDriverArea:
    def __init__(self, car, driver, geoAlert):
        self.car = car
        self.driver= driver 
        self.geoAlert = geoAlert 
def userCarDriverArea(user):
    carDrivers = []
    cars = Car.objects.filter(owner_id=user.id)
    for car in cars:
        driver = car.getPrimaryDriver()
        geoAlert = Alert.objects.filter(car=car).filter(type=Alert.GEOFENCE_ALERT)
        val = CarDriverArea(car, driver, geoAlert)
        carDrivers.append(val)
    return carDrivers

class AreaCircles:
    def __init__(self, area, circles):
        self.area= area 
        self.circles = circles
def userAreaCircles(user):
    areasCircles = []
    areas = AlertArea.objects.filter(owner=user)
    for area in areas:
        circlesAlert = AlertCircle.objects.filter(area=area)
        val = AreaCircles(area, circlesAlert)
        areasCircles.append(val)
    return areasCircles
    
class CarDriverSchedule:
    def __init__(self, car, driver, schedule):
        self.car = car
        self.driver= driver 
        self.schedule = schedule 
def userCarDriverSchedule(user):
    carDrivers = []
    cars = Car.objects.filter(owner_id=user.id)
    for car in cars:
        driver = car.getPrimaryDriver()
        alert = Alert.objects.filter(car=car).filter(type=Alert.SCHEDULE_ALERT)
        if alert:
            schedule = alert[0].schedule_profile
        else:
            schedule = ""
        val = CarDriverSchedule(car, driver, schedule)
        carDrivers.append(val)
    return carDrivers
    
class menuParameters:
    def __init__(self, cars, drivers, user):
        self.cars = cars
        self.drivers= drivers
        self.user = user
        
def initMenuParameters(user):
    cars = Car.objects.filter(owner_id=user.id).filter(is_active=True)
    drivers = Driver.objects.filter(owner_id=user.id).filter(is_active=True)
    menuParams = menuParameters(cars, drivers, user)
    return menuParams

def formatDateStr(date , zeroHour=True):
    hour =  " 00:00:00" if zeroHour else " 23:59:59"
    if not date:
        formatDate = datetime.datetime.now().strftime("%Y-%m-%d")
    else:
        formatDate = date[0:4]+"-"+date[4:6]+"-"+date[6:8] 
    return formatDate + hour 

def makeDateFromDateStr(datestr):
    fmt = "%Y-%m-%d %H:%M:%S"
    return datetime.datetime.strptime(datestr,fmt)
        
class driverLocations:
    def __init__(self, driverPeriod, locationDetailes,isTemporaryDriver):
        self.driverPeriod = driverPeriod
        self.locationDetailes= locationDetailes 
        self.isTemporaryDriver= isTemporaryDriver 
        
    def get_length(self):
        return self.locationDetailes.length()
      
def getLocationsOfPeriod(fromDate,toDate,driverPeriods ,isTemporaryDriver=False):
    driverLocation=[]
    print driverPeriods
    toDate = datetime.datetime.strptime(toDate, '%Y-%m-%d %H:%M:%S')
    fromDate = datetime.datetime.strptime(fromDate, '%Y-%m-%d %H:%M:%S')

    for period in driverPeriods:
        startDate = period.start if period.start.replace(tzinfo=None) > fromDate else fromDate
        if period.end: #not None
            endDate = period.end if period.end.replace(tzinfo=None) < toDate else toDate
        else:
            endDate = toDate
        
        list_of_locations = LocationLog.objects.filter(car=period.car).filter(driver = period.driver).filter(Q(timestamp__gte = startDate) & Q(timestamp__lte = endDate)).order_by('timestamp')
        if list_of_locations:
            val = driverLocations(period,RouteDetails(list_of_locations),isTemporaryDriver)
            driverLocation.append(val)
    print driverLocation
    return driverLocation    
        
        
        
        