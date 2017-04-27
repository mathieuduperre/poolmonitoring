#!/usr/bin/python
############################################
#           pool monitoring
#  read a ph sensor and send to Thingspeak.com
#
#  this use a ph sensor, with a phidget 1030 module
# and an arduino plugged on the raspberry usb port
# so you need UUGear library to speak with the arduino
# and find its unique ID. configure it below.
#
# Author : Mathieu Duperre
# Date   : 25/04/2017
############################################

from time import sleep
from UUGear import *
import time
import RPi.GPIO as GPIO
import sys
import urllib            # URL functions
import urllib2           # URL functions

arduinoID = 'UUGear-Arduino-3186-9458'


################# Default Constants #################
# These can be changed if required
THINGSPEAKKEY = 'XXXXXXXXXX'
THINGSPEAKURL = 'https://api.thingspeak.com/update'

#####################################################

def sendData(url,key,field4,phvalue):
  """
  Send event to internet site
  """
  print("sending data")
  phvalue=str(phvalue)

  values = {'key' : key,'field4' : phvalue}

  postdata = urllib.urlencode(values)
  req = urllib2.Request(url, postdata)

  log = time.strftime("%d-%m-%Y,%H:%M:%S") + ","

  try:
    # Send data to Thingspeak
    response = urllib2.urlopen(req, None, 5)
    html_string = response.read()
    response.close()
    log = log + 'Update ' + html_string

  except urllib2.HTTPError, e:
    log = log + 'Server could not fulfill the request. Error code: ' + str(e.code)
  except urllib2.URLError, e:
    log = log + 'Failed to reach server. Reason: ' + str(e.reason)
  except:
    log = log + 'Unknown error'

  print log


def read_ph_sensor():
    UUGearDevice.setShowLogs(0)
    device = UUGearDevice(arduinoID)

    if device.isValid():
        print "PH Value:"
        raw_input = device.analogRead(3)
        phValue = raw_input * 0.0178
        phValue = phValue - 1.889
        print str(phValue)
        device.detach()
        device.stopDaemon()
        return phValue
    else:
        print 'UUGear device is not correctly initialized.'




phValue=read_ph_sensor()
sendData(THINGSPEAKURL,THINGSPEAKKEY,'field4',phValue)
sys.stdout.flush()
