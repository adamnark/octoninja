from django.contrib import admin
from gpsweb.models import *
from django.http import HttpResponse
from django.core import serializers
from utils.csvSerializer import Serializer as csvSerializer


from pprint import pprint 

def Export_as_json(modeladmin, request, queryset):
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return response
    
def Export_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="%ss.csv"' % queryset[0].__class__.__name__
    serializers.serialize("csv", queryset, stream=response)

    return response

admin.site.add_action(Export_as_csv)
admin.site.add_action(Export_as_json)


class LocationLogAdmin(admin.ModelAdmin):
    list_filter = ('timestamp', 'car', 'driver', )

class AlertLogAdmin(admin.ModelAdmin):
    list_filter = ('notification_sent', 'marked_as_read', 'location_log__car', 'location_log__driver')

class AlertAdmin(admin.ModelAdmin):
    list_filter = ('car', 'type',)
    
class FuelConsumptionLogAdmin(admin.ModelAdmin):
    list_filter = ('car', 'timestamp', 'station_id', ) 

class ManualLogAdmin(admin.ModelAdmin):
    list_filter = ('car', 'driver', 'timestamp', 'log_type', )     



admin.site.register(Unit)
admin.site.register(Person)
admin.site.register(Car)
admin.site.register(Driver)
admin.site.register(PrimaryDriver)
admin.site.register(TemporaryDriver)
admin.site.register(Alert, AlertAdmin)
admin.site.register(AlertLog, AlertLogAdmin)
admin.site.register(LocationLog, LocationLogAdmin)
admin.site.register(FuelConsumptionLog, FuelConsumptionLogAdmin)
admin.site.register(ManualLog, ManualLogAdmin)


#admin.site.register(AlertArea)
#admin.site.register(AlertCircle)
#admin.site.register(AlertScheduleProfile)
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(Site)