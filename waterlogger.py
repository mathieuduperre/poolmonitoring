#!/usr/bin/python
############################################
#           pool monitoring
#  read a float sensor and send to Thingspeak.com
#
# Author : Mathieu Duperre
# Date   : 25/04/2017
############################################

import time
import RPi.GPIO as GPIO
#import os
import sys
import urllib            # URL functions
import urllib2           # URL functions

################# Default Constants #################
# These can be changed if required
THINGSPEAKKEY = 'XXXXXXXXXXX'
THINGSPEAKURL = 'https://api.thingspeak.com/update'
lowsensor_gpio = 27
highsensor_gpio = 15

GPIO.setmode(GPIO.BCM)
GPIO.setup(lowsensor_gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(highsensor_gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#####################################################

def sendData(url,key,field2,field3,lowsensor,highsensor):
  """
  Send event to internet site
  """
  print("sending data")
  lowsensor=str(lowsensor)
  highsensor=str(highsensor)

  values = {'key' : key,'field2' : lowsensor,'field3' : highsensor}

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


def read_low_sensor():
    input_state = GPIO.input(lowsensor_gpio)
    if input_state == False: 
        return 0
    else:
        return 1


def read_high_sensor():
    input_state = GPIO.input(highsensor_gpio)
    if input_state == False:
        return 0
    else:
        return 1


low_floater_state=read_low_sensor()
high_floater_state=read_high_sensor()
print("Low Sensor State: ",low_floater_state)
print("High Sensor State: ",high_floater_state)
sendData(THINGSPEAKURL,THINGSPEAKKEY,'field2','field3',low_floater_state,high_floater_state)
sys.stdout.flush()
