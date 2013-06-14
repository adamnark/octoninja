from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from gpsweb.models import *
from gpsweb.forms import RegistrationForm, LoginForm
import datetime
import csv
from gpsweb.utils import utils
import json

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
    cars = Car.objects.filter(owner_id=user_id).filter(is_active=True)
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

def generateDriverContext(user, driver_id, fromDate=None, toDate=None):
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
    context =  generateDriverContext(request.user, driver_id, fromDate, toDate)
    return render(request, 'driverHistory/driverHistory.html', context)        

@login_required 
def driverHistoryReportCsv(request, driver_id, fromDate=None, toDate=None):
    context =  generateDriverContext(request.user, driver_id, fromDate, toDate)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s-%s-%s.csv"' % (context['driver'], context['fromDateStr'],context['toDateStr'])

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
    context =  generateDriverContext(request.user, driver_id, fromDate, toDate)
    return render(request, 'report/driverReport.html', context)

#####################   Alerts    #####################

def generateAlertsContext(request):
    user = request.user
    user_alerts = Alert.objects.filter(car__owner = user)
    
    if request.method == 'POST': # If the form has been submitted...
        if request.POST.get('alertCheckBox',False):
            chkbxs = request.POST.getlist('alertCheckBox')
            for x in chkbxs:
                alertLog = AlertLog.objects.get(id = int(x))
                alertLog.marked_as_read = True
                alertLog.save()

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
    return context

@login_required 
def alerts(request):
    context = generateAlertsContext(request)
    return render(request, 'alert/alerts.html', context)              

@login_required 
def alertsReportCsv(request):
    context =  generateAlertsContext(request)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Alerts.csv"'
    writer = csv.writer(response)
    writer.writerow(["Alert","Driver","Time"])
    
    alertsArrays = context['alertsArrays']
    for alerts in alertsArrays:
        row = []
        row.append(alerts[0].alert)
        row.append(alerts[0].location_log.driver)
        row.append(alerts[0].location_log.timestamp.strftime('%Y-%m-%d %H:%M'))
        writer.writerow(row)
    return response
    
@login_required 
def alertsReportPrinter(request): 
    context = generateAlertsContext(request)
    return render(request, 'report/alertReport.html', context) 
#####################   Reports    #####################
def generateCarsRouteContext(request, fromDate, toDate):
    user = request.user
    user_id = user.id
    cars = Car.objects.filter(owner_id=user_id)
    fromDateStr = utils.formatDateStr(fromDate)
    toDateStr = utils.formatDateStr(toDate, zeroHour=False)
    totalCarsRoutes = 0
    carsRoutes=[]
    for car in cars:
        list_of_locations = LocationLog.objects.filter(car=car).filter(timestamp__range=[fromDateStr,toDateStr]).order_by('-timestamp')
        routeDetails = utils.RouteDetails(list_of_locations)
        totalCarsRoutes = totalCarsRoutes + routeDetails.length()
        carsRoutes.append(routeDetails)
    context = {
        'user' : user,
        'fromDateStr' : fromDateStr[:-9], # [:-9] truncates the hour
        'toDateStr' : toDateStr[:-9],
        'carsRoutes':carsRoutes,
        'totalCarsRoutes':totalCarsRoutes,
        }
    return context

@login_required 
def carsRoutesCsv(request, fromDate, toDate):
    context = generateCarsRouteContext(request, fromDate, toDate)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="cars-routes-%s-%s.csv"' % (context['fromDateStr'],context['toDateStr'])
    writer = csv.writer(response)
    writer.writerow(["Car","Total Route (Km)","Avg Speed (Kmh)" ,"Max Speed(Kmh)",context['fromDateStr'],context['toDateStr']])
    
    carsRoutes = context['carsRoutes']
    for carRoutes in carsRoutes:
        row = []
        row.append(carRoutes.locationList[0].car)
        row.append(carRoutes.length())
        row.append(carRoutes.avgSpeed())
        row.append(carRoutes.maxSpeed())
        writer.writerow(row)
    return response
def carsRoutesPrinter(request, fromDate, toDate):
    context = generateCarsRouteContext(request, fromDate, toDate)
    return render(request, 'report/carsRoutesReport.html', context)     
    
 
 #####################    PERIMETER     #####################   
@login_required 
def perimeter(request):
    user = request.user
    user_id = user.id
    context = {
        'menuParams' : utils.initMenuParameters(user),
        'user' : user,
        'carsDrivers' : utils.userCarDrivers(user),
        'map_center_lat': '32.047818',
        'map_center_long': '34.761265'
        }
    return render(request, 'perimeter/perimeter.html', context)
 

 
@login_required 
def setPerimeter(request):
    user = request.user
    user_id = user.id
    person = Person.objects.filter(owner=user).filter(is_primary=True)[0]
    message = ''
    
    if request.is_ajax():
        if request.method == 'POST':
            data = json.loads(request.raw_post_data)
            carsId = [int(id) for id in data[0]]
            circles = data[1]
            
            if not carsId:
                message += "<p>No cars were selected.</p>"
            for id in carsId:
                car = Car.objects.get(id=id)
                alert = Alert.objects.filter(car=car).filter(type=Alert.GEOFENCE_ALERT)
                if alert:
                    alert = alert[0]
                    circlesAlert = AlertCircle.objects.filter(alert=alert)
                    for circleAlert in circlesAlert:
                        circleAlert.delete()
                else:
                    alert = Alert(  name="Geo "+str(car),
                                    car=car,
                                    state=datetime.datetime.now(),
                                    cutoff=20,
                                    type=Alert.GEOFENCE_ALERT,
                                    max_speed=0,
                                    schedule_bit_field=0,
                                    )
                    alert.save()
                    alert.recipients.add(person)
                    alert.save()
                
                if not circles:
                    message += '<p>'+str(car)+' - Perimeter was cleared.</p>'
                else:
                    message += '<p>'+str(car)+' - Perimeter was set successfully.</p>'
                    
                for circle in circles:
                    c = AlertCircle(alert=alert,
                                    center_lat=circle["lat"],
                                    center_long=circle["lng"],
                                    radius=circle["rad"],
                                    )
                    c.save()
    
    return HttpResponse(message) 
 
  #####################    schedule     #####################   
@login_required 
def schedule(request):
    user = request.user
    user_id = user.id
    context = {
        'menuParams' : utils.initMenuParameters(user),
        'days':[['Sunday','01'],['Monday','02'], ['Tuesday','03'],['Wednesday','04'], ['Thursday','05'],['Friday','06'],['Saturday','07']],
        'hours':['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23'],
        'user' : user,
        'carsDrivers' : utils.userCarDrivers(user),
    }
    return render(request, 'schedule/schedule.html', context)
 
@login_required 
def setSchedule(request):
    user = request.user
    user_id = user.id
    person = Person.objects.filter(owner=user).filter(is_primary=True)[0]
    message=''
    if request.is_ajax():
        if request.method == 'POST':
            data = json.loads(request.raw_post_data)
            carsId = [int(id) for id in data[0]]
            schedule_bit_field = data[1]
            print 'schedule_bit_field'+schedule_bit_field
            pprint(carsId)
            schedule_bit_field="11"
            if not carsId:
                message += "<p>No cars were selected.</p>"
            
            for id in carsId:
                car = Car.objects.get(id=id)
                alert = Alert.objects.filter(car=car).filter(type=Alert.SCHEDULE_ALERT)
                if alert: #change existing alert
                    alert = alert[0]
                    alert.schedule_bit_field=schedule_bit_field
                    alert.save()
                else:     #create new alert
                    alert = Alert(  name="Schedule "+str(car),
                                    car=car,
                                    state=datetime.datetime.now(),
                                    cutoff=20,
                                    type=Alert.SCHEDULE_ALERT,
                                    max_speed=0,
                                    schedule_bit_field=schedule_bit_field,
                                    )
                    alert.save()
                    alert.recipients.add(person)
                    alert.save()
                
                if schedule_bit_field == 0:
                    message += '<p>'+str(car)+' - Schedule was cleared.</p>'
                else:
                    message += '<p>'+str(car)+' - Schedule was set successfully.</p>'
                    
    print message       
    return HttpResponse(message) 
 