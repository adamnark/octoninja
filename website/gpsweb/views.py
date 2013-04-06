from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from gpsweb.models import Unit, LocationLog, AlertLog
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
    units = Unit.objects.filter(owner_id=user_id)
 
    list_of_locations = []
    for unit in units:
        try:
            last_location = LocationLog.objects.filter(unit_id=unit.id).latest('timestamp')
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
        'units':units,
        'list_of_locations': list_of_locations,
        'user' : user,
        'map_center_lat': map_center_lat,
        'map_center_long': map_center_long,
    }

    return render(request, 'main_map.html', context)

@login_required 
def unit_route(request, unit_id, fromDate=None, toDate=None):
    user = request.user
    user_id = user.id
    units = Unit.objects.filter(owner_id=user_id)
    unit = Unit.objects.filter(owner_id=user_id).filter(id__in=unit_id)
    if not unit:
        return HttpResponseRedirect('/main_map')
    if not fromDate or not toDate:
        list_of_locations = LocationLog.objects.filter(unit_id=unit_id).order_by('timestamp')[:20]
        fromDateStr = datetime.datetime.now().strftime("%Y-%m-%d")
        toDateStr =  datetime.datetime.now().strftime("%Y-%m-%d")
    else:
        fromDateStr = fromDate[0:4]+"-"+fromDate[4:6]+"-"+fromDate[6:8]
        toDateStr =   toDate[0:4]+"-"+toDate[4:6]+"-"+toDate[6:8]
        list_of_locations = LocationLog.objects.filter(unit_id=unit_id).filter(timestamp__range=[fromDateStr+" 00:00:00",toDateStr+" 23:59:59"])
    map_center_lat = '32.047818'
    map_center_long = '34.761265'
    context = {
        'fromDateStr' : fromDateStr,
        'toDateStr' : toDateStr,
        'units':units,
        'list_of_locations': list_of_locations,
        'user' : user,
        'unit': unit[0],
        'map_center_long' : map_center_long,
        'map_center_lat' : map_center_lat,
    }

    return render(request, 'unit_route.html', context) 
    
@login_required 
def user_unit_alerts(request, fromDate=None, toDate=None):
    user = request.user
    user_id = user.id
    units = Unit.objects.filter(owner_id=user_id)
    latest_unit_alarms = []
    list_of_alert_locations = []
    for unit in units:
        try:
            if not fromDate or not toDate:
                latest_unit_alarms = AlertLog.objects.filter(location_log__unit_id=unit.id).order_by('location_log__timestamp')[:20]
                fromDateStr = datetime.datetime.now().strftime("%Y-%m-%d")
                toDateStr =  datetime.datetime.now().strftime("%Y-%m-%d")
            else:
                fromDateStr = fromDate[0:4]+"-"+fromDate[4:6]+"-"+fromDate[6:8]
                toDateStr =   toDate[0:4]+"-"+toDate[4:6]+"-"+toDate[6:8]
                latest_unit_alarms = AlertLog.objects.filter(location_log__unit_id=unit.id).filter(location_log__timestamp__range=[fromDateStr+" 00:00:00",toDateStr+" 23:59:59"])
                
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
        'units':units,
        'list_of_alert_locations': list_of_alert_locations,
        'user' : user,
        'map_center_lat': map_center_lat,
        'map_center_long': map_center_long,
    }

    return render(request, 'units_alerts.html', context)
