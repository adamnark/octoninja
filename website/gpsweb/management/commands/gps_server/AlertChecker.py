'''
Created on 19 במרס 2013

@author: Adam
'''
from gpsweb.models import *

class AlertChecker(object):
    '''
    given a location log entry, checks for any alerts that need to 'go off'.
    will call emailer and/or smser as needed.
    '''


    def __init__(self, LocationLog):
        '''
        Constructor
        '''
        self.locationLog = LocationLog
        
        
    def checkForAlarms(self):
        pass
    