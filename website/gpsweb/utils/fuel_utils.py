import csv
from gpsweb.models import FuelConsumptionLog, Car
import datetime
from django.utils.timezone import utc


def handle_usage_file(csv_file):
    reader = csv.DictReader(csv_file)
    if not validate_file(reader):
        raise Exception("Invalid fuel consumption file!")
    for row in reader:
        update_or_create_row(row)
        
def validate_file(reader):
    return True

    
def update_or_create_row(row):
    car_name = row['car number'].replace('-','')
    timestamp = row['timestamp']
    price_per_liter = float(row['price_per_liter'])
    station_id = int(row['station_id'])
    kilometrage = int(row['kilometrage'])
    print '*'*10 + timestamp
    liters = int(row['liters'])
    
    date = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").replace(tzinfo=utc)
    fuel_row = FuelConsumptionLog.objects.filter(car__name=car_name, timestamp=date)
    
    if fuel_row:
        update_existing_row(fuel_row, liters)
    else: 
        create_new_row(car_name, liters, date, price_per_liter, station_id, kilometrage)


def update_existing_row(fuel_row, liters):
    fuel_row[0].liters = liters
    fuel_row[0].save()

        
def create_new_row(car_name, liters, date, price_per_liter, station_id, kilometrage):
    car = Car.objects.filter(name=car_name)
    if car:
        new_row = FuelConsumptionLog()
        new_row.car = car[0]
        new_row.liters = liters
        new_row.timestamp = date
        new_row.price_per_liter = price_per_liter
        new_row.station_id = station_id
        new_row.kilometrage = kilometrage
        
        new_row.save()
        
        
        