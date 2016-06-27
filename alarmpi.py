#!/usr/bin/env python

#--------------------------------------------------------------------------
# Python to manage garage alarms and door bell
# sends notification out to Instapush
# logs CLIMATE to RRD
# Open/Close may be reversed is code started WITH THE DOOR OPEN/CLOSED
# KFREEGARD/NORTHWARKS 2016
# Version 1.0 23.06.2016
# USE AT YOUR OWN RISK - DON'T RISK/PROTECT LIFE/CRITICAL ASSESTS WITH IT!
#--------------------------------------------------------------------------

#External Imports
import RPi.GPIO as GPIO
import time
from time import sleep
import datetime
import Adafruit_DHT
import traceback
from threading import Thread, Event
import sys
from instapush import Instapush, App
import rrdtool
from rrdtool import update as rrd_update
import urllib2
import os

#Define Instapush App Details
app = App(appid=‘SOMESECRETKEY’, secret=‘SOMESECRETKEY’)

#Define GPIO Numbering
GPIO.setmode(GPIO.BCM)

#---------- GPIO SETUP------
#Define individual GPIO Pins
PIN_GARAGE_DOOR = 17
PIN_DOOR_BELL = 21
PIN_SHUT_DOWN = 18
PIN_WIFI_LED = 19
PIN_TEMP_HUMID = 4 #ONLY HERE AS A REMARK AS DHT Module sets GPIO as 4

#Setup GPIO Pins
GPIO.setup(PIN_GARAGE_DOOR, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # set 17 as input with pull up res
GPIO.setup(PIN_DOOR_BELL, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # set 21 as input with pull up res
GPIO.setup(PIN_SHUT_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # set 18 as input with pull up res
GPIO.setup(PIN_WIFI_LED, GPIO.OUT)

#Define Variables
global OPEN_TIME
global CLOSE_TIME
global TIME_DIFF
global DOOR_TRIGGER
global WIFI_IS_UP
DOOR_TRIGGER = True
WIFI_IS_UP = False

#----------------------------
# Define a threaded callback function to 
# run in another thread when events are detected
# needs GPIO.BOTH to catch both up/down (open/close)  
def garage_callback(channel):
  global DOOR_TRIGGER
  while True:
      if GPIO.input(PIN_GARAGE_DOOR): # if door is opened
          if (DOOR_TRIGGER):
            door_open()
            DOOR_TRIGGER = False # make sure it doesn't fire again
	    return
      if not GPIO.input(PIN_GARAGE_DOOR): # if door is closed
          if not (DOOR_TRIGGER):
            door_close()
            DOOR_TRIGGER = True # make sure it doesn't fire again
            return
#---------------------------
#Define a threaded callback to watch the doorbell
def door_callback(channel):
  door_bell()
#----------------------------
# function for door open
def door_open():
    #get open time
    global OPEN_TIME
    OPEN_TIME = datetime.datetime.now().replace(microsecond=0)
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    alertmsg = timestamp + " - Garage Door Open!"
    global alert_type 
    alert_type = "GarageDoorAlert"
    Send_Alert(alert_type, alertmsg)
#---------------------------- 
# function for door close
def door_close():
    global CLOSE_TIME
    global OPEN_TIME
    CLOSE_TIME = datetime.datetime.now().replace(microsecond=0)
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')	
    alertmsg = timestamp + " - Garage Door Closed"
    global alert_type 
    alert_type = "GarageDoorAlert" 
    Send_Alert(alert_type, alertmsg)
    calc_time(CLOSE_TIME, OPEN_TIME)
#---------------------------
#function for door bell
def door_bell():
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    alertmsg = timestamp + " - Door Bell!"
    global alart_type 
    alert_type = "DoorBell"
    Send_Alert(alert_type, alertmsg)	
#---------------------------

# lets set some initial time values
# prevent a crash on initial start
def set_initial_time():
  global CLOSE_TIME
  global OPEN_TIME
  CLOSE_TIME = datetime.datetime.now().replace(microsecond=0)
  OPEN_TIME = datetime.datetime.now().replace(microsecond=0)

def calc_time(T1, T2):
    difference = T1 - T2
#    print ("Garage Door Open for - " + str(difference))
    OPEN_FOR = ("Garage Door Open for - " + str(difference))
    WriteAlarmLog(OPEN_FOR)
#reset times
    OPEN_TIME = 0
    CLOSE_TIME = 0
    return
#---- send notification--------
def SendAlertMod(ALERT_TYPE, ALERT_MESSAGE):
  if (app.notify(event_name= ALERT_TYPE, trackers={ 'message': ALERT_MESSAGE})) is True:
   print ALERT_MESSAGE
  else:
   print "Error sending notification to Instapush"
#------------------------------
def WriteClimateLog(TEMPERATURE, HUMIDITY):
  FILEPATH = "/home/pi/scripts/log/climate.log"	
  fh = open(FILEPATH, "a")
  fh.write(str(TEMPERATURE))
  fh.write("\n")
  fh.write(str(HUMIDITY))
  fh.write("\n")
  fh.close
  return	
#------------------------------
#write to RRD file
def WriteRRD(TEMP, HUM):
  FILEPATH = "/home/pi/scripts/log/garage_climate.rrd"
  TEMP=float(TEMP)
  HUM=float(HUM)
  rrd_update(FILEPATH, 'N:%s:%s' %(TEMP, HUM))
#------------------------------
def WriteAlarmLog(ALARM):
 FILEPATH = "/home/pi/scripts/log/alarm.log"
 fh = open(FILEPATH, "a")
 fh.write(ALARM)
 fh.write("\n")
 fh.close
 return
#------------------------------
# Centralise alert message logging and sending
def Send_Alert(ALERT_TYPE, ALERT_MESSAGE):
 app.notify(event_name= ALERT_TYPE, trackers={ 'message': ALERT_MESSAGE})
 #Append alarm log
 WriteAlarmLog(ALERT_MESSAGE)
 print ALERT_MESSAGE
#--------------------------
# Get temp/Hum
# DHT22_PIN = GPIO4

class PeriodicThread(Thread):
    def __init__(self, interval):
        self.stop_event = Event()
        self.interval = interval
        super(PeriodicThread, self).__init__()
    def run(self):
         while not self.stop_event.is_set():
             self.main()
             # wait self.interval seconds or until the stop_event is set
             self.stop_event.wait(self.interval)        
    def terminate(self):
        self.stop_event.set()
    def main(self):
       print('Replaced with subclass')

class GetClimate(PeriodicThread):
    def main(self):
       timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
       humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
       if temperature is not None and humidity is not None:
           self.temperature = timestamp + ' - Temperature: {:.1f} C'.format(temperature)
           self.humidity = timestamp + ' - Humidity:    {:.1f} %'.format(humidity)
	   WriteRRD(round(temperature,1), round(humidity,1)) 
#	   WriteClimateLog(self.temperature, self.humidity)

class GetWIFI(PeriodicThread):
    def main(self):
      global WIFI_IS_UP
      if Internet_On() == 1 and not WIFI_IS_UP:
 	timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        IsWIFIup = timestamp + ' - WiFi Up'
        WriteAlarmLog(IsWIFIup)
        WIFI_IS_UP = True
        GPIO.output(PIN_WIFI_LED,True)
      elif Internet_On() == 0:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        IsWIFIup = timestamp + ' - WiFi Down!'
        WriteAlarmLog(IsWIFIup)
	WIFI_IS_UP = False
        GPIO.output(PIN_WIFI_LED,False)
      else:
        pass

#Check for gateway up - do it just once.
def Internet_On():
  loop_value = 1
  while (loop_value == 1):
    try:
        response=urllib2.urlopen('http://192.168.1.1',timeout=1)
        return True
    except urllib2.URLError as err: pass
    return False
  loop_value = 0

def Shutdown(channel):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    IsShutDown = timestamp + ' - Shutting Down AlarmPI !'
    WriteAlarmLog(IsShutDown)  
    os.system("sudo shutdown -h now")  
       
#----------------------------------------------
#Setup GPIO Threaded Pins
#HAS to be after the callback function 
#GPIO.both Looks for both up/down (open/close door)and calls callback function with debounce(ms) to stop repeats
GPIO.add_event_detect(PIN_GARAGE_DOOR, GPIO.BOTH, callback=garage_callback, bouncetime=2000)
GPIO.add_event_detect(PIN_DOOR_BELL, GPIO.FALLING, callback=door_callback, bouncetime=2000)
GPIO.add_event_detect(PIN_SHUT_DOWN, GPIO.FALLING, callback = Shutdown, bouncetime = 2000)
#============================================================================

#Runs non-stop
# worker thread is a subclass of Periodic class, GetClimate just replaces the def main.
def main():
    try:
      worker = GetClimate(interval=900)#15mins
      worker.start()
      worker1 = GetWIFI(interval=300)#5mins
      worker1.start()
      set_initial_time()
      print "..Ready"
      while True:
       time.sleep(1)    
    except KeyboardInterrupt:
        print "Shutdown requested...exiting"
        GPIO.cleanup()
        worker.terminate()
        worker1.terminate()
    except Exception:
        traceback.print_exc(file=sys.stdout)
        GPIO.cleanup()
        worker.terminate()
        worker1.terminate()
        sys.exit(0)

if __name__ == "__main__":
    main()
