from gpsweb.models import *
from gpsweb.utils import utils
import datetime

class DriverInfo:
    def __init__(self, driver_context):
            self.driver = driver_context["driver"]
            self.total_length = driver_context["total_length"]
            self.alerts_count = driver_context["alerts_count"] 
            

class UserInfo:
    def __init__(self, user):
        self.user = user
        self.drivers = []
        self.total_length = 0
        self.alerts_count = 0
        
    def add(self, driverinfo):
        self.drivers.append(driverinfo)
        self.total_length += driverinfo.total_length
        self.alerts_count += driverinfo.alerts_count
        
    
            
def report():
    users = Person.objects.filter(is_primary=True)
    today = datetime.today().strftime("%Y%m%d")
    for user in users:
        user_info = aggregate_user_info(user)
        send_report(user_info)

        
def aggregate_user_info(user):
    drivers = Driver.objects.filter(owner=user)
    user_info = UserInfo(user)
    for driver in drivers:
        driver_context = generateDriverContext(user, driver.id, fromDate=today, toDate=today)
        di = DriverInfo(driver_context)
        user_info.add(di)
        
    return user_info

    
def send_report(user_info):
        pass
        