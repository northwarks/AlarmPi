# AlarmPi
Python script for monitoring my garage, could be used for anything really, uses Instapush to send notifications to my phone.
Has 2 GPIO for the door and door bell,has a climate section, uses RRD tool to save climate data. Has first stabs at threading. 
As this code is on a headless Pi Zero inside my alarm panel I've added status LEDs and buttons to shutdown/restart 
the Pi instead of having to remove the cover.
