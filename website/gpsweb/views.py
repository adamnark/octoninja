from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from gpsweb.models import *
from gpsweb.forms import RegistrationForm, LoginForm
import datetime
from gpsweb.utils import utils

from pprint import pprint

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
        return HttpResponseRedirect('/main')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/main')
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
#####################    Main View     ##################### 
@login_required
def mainView(request):
    user = request.user
    user_id = user.id
    cars = Car.objects.filter(owner_id=user_id)
    list_of_locations = []
    for car in cars:
        try:
            last_location = LocationLog.objects.filter(car=car).latest('timestamp')
        except LocationLog.DoesNotExist:
            pass
        else:
            list_of_locations.append(last_location)

    context = {
        'menuParams' : utils.initMenuParameters(user),
        'list_of_locations': list_of_locations,
        'user' : user,
        'map_center_lat': '32.047818',
        'map_center_long': '34.761265',
    }
    return render(request, 'mainView/mainView.html', context)
#####################    Car History     #####################
@login_required 
def carHistory(request, car_id, fromDate=None, toDate=None):
    user = request.user
    user_id = user.id
    car = Car.objects.filter(owner_id=user_id).filter(id__in=car_id)
    if not car:
        return HttpResponseRedirect('/')

    fromDateStr = utils.formatDateStr(fromDate)
    toDateStr = utils.formatDateStr(toDate, zeroHour=False)
        
    list_of_locations = LocationLog.objects.filter(car=car).filter(timestamp__range=[fromDateStr,toDateStr]).order_by('-timestamp')
    

    context = {
        'menuParams' : utils.initMenuParameters(user),
        'fromDateStr' : fromDateStr[:-9], # [:-9] truncates the hour
        'toDateStr' : toDateStr[:-9],
        'route_details':utils.RouteDetails(list_of_locations),
        'user' : user,
        'car': car[0],
        'primary_driver' : car[0].getPrimaryDriversByDateRange(fromDateStr,toDateStr),
        'temporary_drivers' : car[0].getTemporaryDriversByDateRange(fromDateStr,toDateStr),
        'map_center_lat' : '32.047818',
        'map_center_long' : '34.761265',
    }

    return render(request, 'carHistory/carHistory.html', context)         
    
#####################    Driver History     #####################   

def generateDriverContext(request, driver_id, fromDate=None, toDate=None):
    user = request.user
    user_id = user.id
    driver = Driver.objects.filter(owner_id=user_id).filter(id__in=driver_id)
    if not driver:
        return HttpResponseRedirect('/')
    fromDateStr = utils.formatDateStr(fromDate)
    toDateStr = utils.formatDateStr(toDate, zeroHour=False)
    #Need to get all primary\temporary of the driver in this dates

    temporary = TemporaryDriver.objects.filter(driver = driver).filter(Q(end__gte = fromDateStr) | Q(start__lte = toDateStr))
    temporaryPeriodsLocations = utils.getLocationsOfPeriod(fromDateStr, toDateStr, temporary, isTemporaryDriver=True)
    primary = PrimaryDriver.objects.filter(driver = driver).filter(Q(end__gte = fromDateStr) | Q(end = None) )
    primaryPeriodsLocations = utils.getLocationsOfPeriod(fromDateStr, toDateStr, primary)
    periodsLocations =  temporaryPeriodsLocations + primaryPeriodsLocations
    total_length = 0
    for period in periodsLocations:
        total_length += period.get_length()
        
    alerts = AlertLog.objects.filter(location_log__driver = driver[0]).filter(Q(location_log__timestamp__gte = fromDateStr) & Q(location_log__timestamp__lte = toDateStr)).filter(notification_sent = True)
    
    context = {
        'menuParams' : utils.initMenuParameters(user),
        'fromDateStr' : fromDateStr[:-9], # [:-9] truncates the hour
        'toDateStr' : toDateStr[:-9],
        'fromDate' : fromDate, 
        'toDate' : toDate,
        'periodsLocations' : periodsLocations,
        'total_length':total_length,
        'alerts_count':len(alerts),
        'user' : user,
        'driver' : driver[0],
        'map_center_lat' : '32.047818',
        'map_center_long' : '34.761265',
    }
    
    return context


@login_required 
def driverHistory(request, driver_id, fromDate=None, toDate=None):   
    context =  generateDriverContext(request, driver_id, fromDate, toDate)
    return render(request, 'driverHistory/driverHistory.html', context)        

@login_required 
def driverHistoryReportCsv(request, driver_id, fromDate=None, toDate=None):
    context =  generateDriverContext(request, driver_id, fromDate, toDate)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s-%s-%s.csv"' % (context['driver'], context['fromDateStr'],context['toDateStr'])
    
    import csv
    #from datetime import date
    
    writer = csv.writer(response)
    writer.writerow(["Start","End","Car","Distance Traveled",])
    
    periodsLocations = context['periodsLocations']
    for period in periodsLocations:
        row = []
        row.append(period.driverPeriod.start.strftime('%Y-%m-%d'))
        if period.driverPeriod.end:
            row.append(period.driverPeriod.end.strftime('%Y-%m-%d'))
        else:
            row.append('')
        row.append(period.driverPeriod.car)
        row.append(period.locationDetailes.length())
        
        writer.writerow(row)

    return response
    
@login_required 
def driverHistoryReportPrinter(request, driver_id, fromDate=None, toDate=None):    
    context =  generateDriverContext(request, driver_id, fromDate, toDate)
    return render(request, 'report/driverReport.html', context)

#####################   Alerts    #####################
@login_required 
def alerts(request):
    user = request.user
    user_alerts = Alert.objects.filter(car__owner = user)
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            alertCheckBoxes = form.cleaned_data['alertCheckBox']
			for alertId in alertCheckBoxes:
				print alertId

            
    
    groups = []
    for user_alert in user_alerts:
        alerts_logs = AlertLog.objects.filter(alert = user_alert).filter(marked_as_read = False).order_by('location_log__timestamp')
        group = []
        for alert_log in alerts_logs:
            if alert_log.notification_sent and group:
                groups.append(group)
                group = []
            group.append(alert_log)
        if group:
            groups.append(group)    
    
    context = {
        'menuParams' : utils.initMenuParameters(user),
        'user' : user,
        'map_center_lat' : '32.047818',
        'map_center_long' : '34.761265',
        'alertsArrays':groups,
    }
    return render(request, 'alert/alerts.html', context)              

#####################   Reports    #####################


    
 