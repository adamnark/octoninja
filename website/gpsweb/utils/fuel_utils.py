import csv
from gpsweb.models import FuelConsumption, Car
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
    month = int(row['month'])
    year = int(row['year'])
    liters = int(row['liters'])
    
    date = datetime.datetime(year, month, 1).replace(tzinfo=utc)
    fuel_row = FuelConsumption.objects.filter(car__name=car_name, month=date)
    
    if fuel_row:
        update_existing_row(fuel_row, liters)
    else: 
        create_new_row(car_name, liters, date)


def update_existing_row(fuel_row, liters):
    fuel_row[0].liters = liters
    fuel_row[0].save()

        
def create_new_row(car_name, liters, date):
    car = Car.objects.filter(name=car_name)
    if car:
        new_row = FuelConsumption()
        new_row.car = car[0]
        new_row.liters = liters
        new_row.month = date
        
        new_row.save()