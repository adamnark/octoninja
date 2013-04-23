from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from gpsweb.models import *
from gpsweb.forms import RegistrationForm, LoginForm
import datetime

def UserRegistration(request):
    if request.user.is_authenticated():
            return HttpResponseRedirect('/main_map')
    if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = User.objects.create_user(username=form.cleaned_data['username'],
                                                password=form.cleaned_data['password'],
                                                email=form.cleaned_data['email'])
                user.save()
                user.first_name=form.cleaned_data['first_name']
                user.last_name=form.cleaned_data['last_name']
                user.save()
                return HttpResponseRedirect('/main_map')
            else:
                return render_to_response('register.html', {'form':form}, context_instance=RequestContext(request))
    else:
            ''' user is not submitting the form, show them a blank registration form '''
            form = RegistrationForm()
            context = {'form': form}
            return render_to_response('register.html', context, context_instance=RequestContext(request))

def UserLogin(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/main_map')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/main_map')
            else:
                return render_to_response('login.html', {'form':form}, context_instance=RequestContext(request))
        else:
            return render_to_response('login.html', {'form':form}, context_instance=RequestContext(request))
    else:
        ''' user is not submitting the form, show them the login form '''
        form = LoginForm()
        context = {'form':form}
        return render_to_response('login.html', context, context_instance=RequestContext(request))

def UserLogout(request):
    logout(request)
    return HttpResponseRedirect('/')
@login_required
def main_map(request):
    user = request.user
    user_id = user.id
    cars = Car.objects.filter(owner_id=user_id)
    drivers = Driver.objects.filter(owner_id=user_id)
    list_of_locations = []
    for car in cars:
        try:
            last_location = LocationLog.objects.filter(car=car).latest('timestamp')
        except LocationLog.DoesNotExist:
            pass
        else:
            list_of_locations.append(last_location)

    if list_of_locations:
        map_center_lat = list_of_locations[0].lat
        map_center_long = list_of_locations[0].long
    else:
        map_center_lat = '32.047818'
        map_center_long = '34.761265'

    context = {
        'cars':cars,
        'drivers':drivers,
        'list_of_locations': list_of_locations,
        'user' : user,
        'map_center_lat': map_center_lat,
        'map_center_long': map_center_long,
    }

    return render(request, 'main_map.html', context)

@login_required 
def unit_route(request, car_id, fromDate=None, toDate=None):
    user = request.user
    user_id = user.id
    cars = Car.objects.filter(owner_id=user_id)
    drivers = Driver.objects.filter(owner_id=user_id)
    car = Car.objects.filter(owner_id=user_id).filter(id__in=car_id)
    if not car:
        return HttpResponseRedirect('/main_map')
    if not fromDate or not toDate:
        fromDateStr = datetime.datetime.now().strftime("%Y-%m-%d")
        toDateStr =  datetime.datetime.now().strftime("%Y-%m-%d")
    else:
        fromDateStr = fromDate[0:4]+"-"+fromDate[4:6]+"-"+fromDate[6:8]
        toDateStr =   toDate[0:4]+"-"+toDate[4:6]+"-"+toDate[6:8]
    list_of_locations = LocationLog.objects.filter(car=car).filter(timestamp__range=[fromDateStr+" 00:00:00",toDateStr+" 23:59:59"]).order_by('-timestamp')
    map_center_lat = '32.047818'
    map_center_long = '34.761265'
    context = {
        'fromDateStr' : fromDateStr,
        'toDateStr' : toDateStr,
        'cars':cars,
        'drivers':drivers,
        'list_of_locations': list_of_locations,
        'user' : user,
        'car': car[0],
        'map_center_long' : map_center_long,
        'map_center_lat' : map_center_lat,
    }

    return render(request, 'unit_route.html', context) 
    
@login_required 
def user_unit_alerts(request, fromDate=None, toDate=None):
    user = request.user
    user_id = user.id
    cars = Car.objects.filter(owner_id=user_id)
    drivers = Driver.objects.filter(owner_id=user_id)
    latest_unit_alarms = []
    list_of_alert_locations = []
    for car in cars:
        try:
            if not fromDate or not toDate:
                fromDateStr = datetime.datetime.now().strftime("%Y-%m-%d")
                toDateStr =  datetime.datetime.now().strftime("%Y-%m-%d")
            else:
                fromDateStr = fromDate[0:4]+"-"+fromDate[4:6]+"-"+fromDate[6:8]
                toDateStr =   toDate[0:4]+"-"+toDate[4:6]+"-"+toDate[6:8]
            latest_unit_alarms = AlertLog.objects.filter(location_log__car=car).filter(location_log__timestamp__range=[fromDateStr+" 00:00:00",toDateStr+" 23:59:59"]).order_by('-location_log__timestamp')
                
        except AlertLog.DoesNotExist:
            pass
        else:
            if latest_unit_alarms:
                list_of_alert_locations.append(latest_unit_alarms)

    map_center_lat = '32.047818'
    map_center_long = '34.761265'

    context = {
        'fromDateStr' : fromDateStr,
        'toDateStr' : toDateStr,       
        'cars':cars,
        'drivers':drivers,
        'list_of_alert_locations': list_of_alert_locations,
        'user' : user,
        'map_center_lat': map_center_lat,
        'map_center_long': map_center_long,
    }

    return render(request, 'units_alerts.html', context)

    
    
@login_required 
def car_alerts(request, fromDate=None, toDate=None):
    return render(request, 'units_alerts.html', context)
@login_required 
def car_history(request, car_id, fromDate=None, toDate=None):
    user = request.user
    user_id = user.id
    cars = Car.objects.filter(owner_id=user_id)
    drivers = Driver.objects.filter(owner_id=user_id)
    car = Car.objects.filter(owner_id=user_id).filter(id__in=car_id)
    if not car:
        return HttpResponseRedirect('/main_map')
    if not fromDate or not toDate:
        fromDateStr = datetime.datetime.now().strftime("%Y-%m-%d")
        toDateStr =  datetime.datetime.now().strftime("%Y-%m-%d")
    else:
        fromDateStr = fromDate[0:4]+"-"+fromDate[4:6]+"-"+fromDate[6:8]
        toDateStr =   toDate[0:4]+"-"+toDate[4:6]+"-"+toDate[6:8]
    list_of_locations = LocationLog.objects.filter(car=car).filter(timestamp__range=[fromDateStr+" 00:00:00",toDateStr+" 23:59:59"]).order_by('-timestamp')
    map_center_lat = '32.047818'
    map_center_long = '34.761265'
    context = {
        'fromDateStr' : fromDateStr,
        'toDateStr' : toDateStr,
        'cars':cars,
        'drivers':drivers,
        'list_of_locations': list_of_locations,
        'user' : user,
        'car': car[0],
        'map_center_long' : map_center_long,
        'map_center_lat' : map_center_lat,
    }
    return render(request, 'car_history.html', context) 
@login_required 
def driver_history(request, fromDate=None, toDate=None):
    return render(request, 'units_alerts.html', context)    