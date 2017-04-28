#!/usr/bin/python
############################################
#           pool monitoring
#  Read data from a DS18B20 sensor and a
#  float sensor and send to Thingspeak.com
#
# Author : Mathieu Duperre
# Date   : 25/04/2017
############################################

import time
import os
import sys
import urllib            # URL functions
import urllib2           # URL functions

################# Default Constants #################
# These can be changed if required
THINGSPEAKKEY = 'XXXXXXXXXXX'
THINGSPEAKURL = 'https://api.thingspeak.com/update'
tmp_sensor_name = '28-000003473299'
base_dir = '/sys/bus/w1/devices/'
#####################################################

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

def sendData(url,key,field1,temp):
  """
  Send event to internet site
  """
  print("sending data")
  temp=str(temp)

  values = {'key' : key,'field1' : temp}

  postdata = urllib.urlencode(values)
  req = urllib2.Request(url, postdata)

  log = time.strftime("%d-%m-%Y,%H:%M:%S") + ","
  #log = log + "{:.1f}C".format(temp) + ","
  #log = log + "{:.2f}mBar".format(level) + ","

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


def read_temp_raw():
    global device_file
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        #return temp_c, temp_f
        return temp_f


device_folder = base_dir + tmp_sensor_name
device_file = device_folder + '/w1_slave'
temperature=read_temp()
print("temp: ",temperature)
sendData(THINGSPEAKURL,THINGSPEAKKEY,'field1',temperature)
sys.stdout.flush()
