# AlarmPi
Python script for monitoring my garage, could be used for anything really, uses Instapush to send notifications to my phone, quick and dirty. Has 2 GPIO for the door and door bell,has a climate section, uses RRD tool to save climate data. Has first stabs at threading. Outputs to a log so I can see log of open/close and duration, also logs wifi up/down.

As this code is on a headless Pi Zero inside my alarm panel I've added status LEDs and buttons to shutdown/restart 
the Pi instead of having to remove the cover. Status of the Pi, shows red when its got power and a green LED to show the wifi is up and running - it pings my gateway. I can see at a glance at the panel all is well. I can access the Pi over SSH.

I've used a magnetic normally closed reed contact on the door and it works just fine

KNOWN ISSUES
Worth adding my code won't be the best you have seen, it works for me. This code has been very reliabe on my Pi, only known issue is the door miss-reports the door as open when it closes if the Pi is reset with the door open, I just reset the Pi with the door closed and all is fine.
