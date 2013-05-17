from math import sin, cos, radians, degrees, acos
from gpsweb.models import *
import datetime
def calc_dist(lat_a, long_a, lat_b, long_b):
    lat_a = float(lat_a)
    long_a = float(long_a)
    lat_b = float(lat_b)
    long_b = float(long_b)
    
    multiplier = 6371 # for kilometers
    #multiplier = 3959 # for miles
    return ( multiplier *
    acos(
        cos( radians(lat_a) ) *
        cos( radians(lat_b) ) *
        cos( radians(long_b) - radians(long_a) ) +
        sin( radians(lat_a) ) * sin( radians(lat_b) )
        )
    )
    

    
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
        prev_location = self.locationList[0]
        for curr_location in self.locationList:
            dist += calc_dist(  prev_location.lat,
                                prev_location.long,
                                curr_location.lat,
                                curr_location.long)
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

class menuParameters:
    def __init__(self, cars, drivers):
        self.cars = cars
        self.drivers= drivers
def initMenuParameters(user):
    cars = Car.objects.filter(owner_id=user.id)
    drivers = Driver.objects.filter(owner_id=user.id)
    menuParams = menuParameters(cars, drivers)
    return menuParams

def formatDateStr(date , zeroHour=True):
    hour =  " 00:00:00" if zeroHour else " 23:59:59"
    if not date:
        formatDate = datetime.datetime.now().strftime("%Y-%m-%d")
    else:
        formatDate = date[0:4]+"-"+date[4:6]+"-"+date[6:8] 
    return formatDate + hour 
        
        
class driverLocations:
    def __init__(self, driverPeriod, locationList):
        self.driverPeriod = driverPeriod
        self.locationList= locationList 
def getLocationsOfPeriod(fromDate,toDate,driverPeriods):
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
        
        list_of_locations = LocationLog.objects.filter(car=period.car).filter(driver = period.driver).filter(Q(timestamp__gte = startDate) & Q(timestamp__lte = endDate)).order_by('-timestamp')
        if list_of_locations:
            val = driverLocations(period,list_of_locations)
            driverLocation.append(val)
    print driverLocation
    return driverLocation    
        
        
        
        