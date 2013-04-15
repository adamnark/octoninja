from django.contrib import admin
#from django.contrib.auth.models import User
from gpsweb.models import *


#admin.site.register(GpsUser)
admin.site.register(Unit)
admin.site.register(Person)
admin.site.register(Car)
admin.site.register(Driver)
admin.site.register(TemporaryDriver)
admin.site.register(Alert)
admin.site.register(LocationLog)
admin.site.register(AlertLog)
