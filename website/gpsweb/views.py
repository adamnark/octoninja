from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from gpsweb.models import Unit, LocationLog

def index(request, user_id):
    units = Unit.objects.filter(owner_id=user_id)
    user = User.objects.filter(pk=user_id)[0]
    list_of_locations = []
    for unit in units:
        list_of_locations.append(LocationLog.objects.filter(unit_id=unit.id).order_by('-timestamp')[0])

    if list_of_locations: 
        map_center_lat = list_of_locations[0].lat
        map_center_long = list_of_locations[0].long
    else: 
        map_center_lat = '32.047818' 
        map_center_long = '34.761265'

    context = {
        'list_of_locations': list_of_locations,
        'user' : user,
        'map_center_lat': map_center_lat,
        'map_center_long': map_center_long,
    }

    return render(request, 'index.html', context)
