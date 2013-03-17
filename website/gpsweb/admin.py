from django.contrib import admin
#from django.contrib.auth.models import User
from gpsweb.models import *

#admin.site.register(User)
admin.site.register(Unit)
admin.site.register(Recipient)
admin.site.register(SpeedAlert)
admin.site.register(LocationLog)
admin.site.register(AlertLog)
