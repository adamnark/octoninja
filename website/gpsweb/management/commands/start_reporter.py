from django.core.management.base import BaseCommand, CommandError
from reporter import reporter

class Command(BaseCommand):
    help = 'Generates a report for each user and emails them. No arguments.'

    def handle(self, *args, **options):
        if len(args) != 0:
            raise CommandError('No arguments please!')
        reporter.test()
        


total distance traveled today: 435135135131km
        
shevac:
    alerts triggered count
    max speed
    total distance travelled
        
shevac:
    alerts triggered count
    max speed
    total distance travelled
        
shevac:
    alerts triggered count
    max speed
    total distance travelled
        
shevac:
    alerts triggered count
    max speed
    total distance travelled
    