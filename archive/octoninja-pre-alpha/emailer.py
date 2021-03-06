import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os

#args_dict = {"nickname":"adam", 
#             "unit_name":"car 1", 
#             "speed":"0", 
#             "location":"32.09150335%2034.788823",
#             "format":"hello, %(name)s! %(unit_name)s was going......."
#             "timestamp":datetime.datetime.now(),
#             "to":"amir_solav@gmail.com"}

def mail(args_dict): #args_dict has at least: timestamp, name, unit_name, location, format
    gmail_user = "GPSMonitorEmailer@gmail.com"
    gmail_pwd = "adam123456"
    message = MIMEMultipart('alternative')
    message['Subject'] = 'GPS Alert has gone off!'
    message['From'] = gmail_user
    message['To'] = args_dict['to']
    message.attach(MIMEText(args_dict["format"] % args_dict, 'html'))
    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user, gmail_pwd)
    mailServer.sendmail(gmail_user, args_dict['to'], message.as_string())
    # Should be mailServer.quit(), but that crashes...
    mailServer.close()

#if __name__ == '__main__': main()


