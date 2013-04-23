from django.core.management.base import BaseCommand, CommandError
from gpsweb.models import *


from gps_server import ModelWriter

class Command(BaseCommand):
    def handle(self, *args, **options):
    
        alert = Alert.objects.filter(id=2)[0]
        for recipient_ in alert.recipients.all():
            recipient = recipient_
        locationLog = LocationLog.objects.filter(id=5)[0]
        ModelWriter.sendSms(locationLog, alert, recipient)
        print 'everything went well, amir'