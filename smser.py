'''
Created on Jan 22, 2013

@author: Adam Narkunski
'''
#!/usr/bin/env python
"""
sms.py - Used to send txt messages.
"""
import serial
import time

class TextMessage:
    def __init__(self, recipient="0123456789", message="TextMessage.content not set."):
        self.recipient = recipient
        self.content = message
 
    def setRecipient(self, number):
        self.recipient = number
 
    def setContent(self, message):
        self.content = message
 
    def connectPhone(self):
        win_port = 'COM3'
        #linux_port = '/dev/ttyACM0'
        self.ser = serial.Serial(win_port, 9600, timeout=5)
        print 'connected!\n', self.ser
        time.sleep(1)
 
    def sendMessage(self):
        self.ser.write('ATZ\r')
        time.sleep(1)
        self.ser.write('AT+CMGF=1\r')
        time.sleep(1)
        self.ser.write('''AT+CMGS="''' + self.recipient + '''"\r''')
        time.sleep(1)
        self.ser.write(self.content + "\r")
        time.sleep(1)
        self.ser.write(chr(26))
        time.sleep(1)
 
    def disconnectPhone(self):
        self.ser.close()

smser = TextMessage(recipient='0545949562', message='kaki matok\n from python w/ love')
smser.connectPhone()
smser.sendMessage()
smser.disconnectPhone()
