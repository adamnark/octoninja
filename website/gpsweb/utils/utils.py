from math import sin, cos, radians, degrees, acos
from gpsweb.models import *

def calc_dist(lat_a, long_a, lat_b, long_b):
    lat_a = radians(lat_a)
    lat_b = radians(lat_b)
    long_diff = radians(long_a - long_b)
    distance = (sin(lat_a) * sin(lat_b) +
                cos(lat_a) * cos(lat_b) * cos(long_diff))
    return degrees(acos(distance)) * 69.09
	
def car_dist(car_id, fromDate, toDate)
	cars = Car.objects.filter(id=car_id)
	dist = 0
	if cars:
		car = cars[0]
	else:
		return dist
	if not fromDate or not toDate:
		list_of_locations = LocationLog.objects.filter(car=car).order_by('-timestamp')
	else:
		list_of_locations = LocationLog.objects.filter(car=car).filter(timestamp__range=[fromDate,toDate]).order_by('-timestamp')
	
	if not list_of_locations:
		return dist

	prev_location = list_of_locations[0]
	for curr_location in list_of_locations:
		dist += calc_dist(prev_location.lat ,prev_location.long ,cur_location.lat ,curr_location.long)
	return dist