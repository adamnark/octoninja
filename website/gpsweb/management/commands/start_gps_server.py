from django.core.management.base import BaseCommand, CommandError
from gpsweb.models import *
from gps_server import Server

default_port = 9000

class Command(BaseCommand):
    args = '<port>'
    help = 'Starts the gps server on specified port. defalt is %d' % default_port

    def handle(self, *args, **options):
        if len(args) > 1:
            raise CommandError('too many arguments!')
        port = args[0] if args else default_port

        # change this line to 
        serv = Server.Server()
        serv.start() 
        #Serversta.test_func(port)
