#!/usr/bin/python
############################################
#           pool monitoring
#  read an orp sensor and send to Thingspeak.com
#
# Author : Mathieu Duperre
# Date   : 25/04/2017
############################################
import sys; sys.path.append('/home/pi/poolmonitoring/')

#from time import sleep
from UUGear import *
import time
import RPi.GPIO as GPIO
import sys
import urllib            # URL functions
import urllib2           # URL functions

arduinoID = 'UUGear-Arduino-3186-9458'


################# Default Constants #################
# These can be changed if required
THINGSPEAKKEY = 'XXXXXXXXXXXXX'
THINGSPEAKURL = 'https://api.thingspeak.com/update'

#####################################################

def sendData(url,key,field5,orpvalue):
  """
  Send event to internet site
  """
  print("sending data")
  orpvalue=str(orpvalue)

  values = {'key' : key,'field5' : orpvalue}

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


def read_orp_sensor():
    UUGearDevice.setShowLogs(0)
    device = UUGearDevice(arduinoID)

    if device.isValid():
        print "ORP Value:"
        raw_input = device.analogRead(5)
        orpValue = float(raw_input) / 200
        orpValue = 2.5 - orpValue
        orpValue = float(orpValue) / 1.037
        orpValue = orpValue * 1000
        orpValue = round(orpValue,2)
        print str(orpValue)
        device.detach()
        device.stopDaemon()
        return orpValue
    else:
        print 'UUGear device is not correctly initialized.'




orpValue=read_orp_sensor()
sendData(THINGSPEAKURL,THINGSPEAKKEY,'field5',orpValue)
sys.stdout.flush()
