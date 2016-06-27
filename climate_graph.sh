#!/bin/bash
now=$(date +%s)
now_formatted=$(date +%s | awk '{printf "%s\n", strftime("%c",$1)}' | sed -e 's/:/\\:/g')

RRDPATH="/home/pi/scripts/log/"
IMGPATH="/home/pi/scripts/log/"
RAWCOLOUR="#FF0000"
RAWCOLOUR2="#40ff00"
RRDFILE="garage_climate.rrd"

#day
rrdtool graph $IMGPATH/day.png --start -24h \
--full-size-mode \
--width=700 --height=400 \
--slope-mode \
--color=SHADEB#9999CC \
--title="Garage Climate Day" \
--watermark="Garage Climate" \
--vertical-label='Temp(°C) Humid(%)' \
--upper-limit=100 \
--lower-limit=0 \
DEF:temp1=$RRDPATH/$RRDFILE:temp:AVERAGE \
DEF:humid1=$RRDPATH/$RRDFILE:humid:AVERAGE \
VDEF:TempMin=temp1,MINIMUM \
VDEF:TempMax=temp1,MAXIMUM \
VDEF:HumMin=humid1,MINIMUM \
VDEF:HumMax=humid1,MAXIMUM \
LINE1:temp1$RAWCOLOUR:"Temp" \
LINE2:humid1$RAWCOLOUR2:"Humidity" \
COMMENT:" \\n" \
GPRINT:temp1:MAX:"Temp Max - %8.1lf%sc" \
COMMENT:" \\n" \
GPRINT:temp1:MIN:"Temp Min - %8.1lf%sc" \
COMMENT:" \\n" \
GPRINT:humid1:MAX:"Humidity Max - %4.1lf%s%%" \
COMMENT:" \\n" \
GPRINT:humid1:MIN:"Humidity Min - %4.1lf%s%%" \
COMMENT:" \\n" \
COMMENT:" \\n" \
COMMENT:"Created at $now_formatted"


#hour
rrdtool graph $IMGPATH/hour.png --start -1h \
--full-size-mode \
--width=700 --height=400 \
--slope-mode \
--color=SHADEB#9999CC \
--title="Garage Climate Hour" \
--watermark="Garage Climate" \
--vertical-label='Temp(°C) Humid(%)' \
--upper-limit=100 \
--lower-limit=0 \
DEF:temp1=$RRDPATH/$RRDFILE:temp:AVERAGE \
DEF:humid1=$RRDPATH/$RRDFILE:humid:AVERAGE \
VDEF:TempMin=temp1,MINIMUM \
VDEF:TempMax=temp1,MAXIMUM \
LINE1:temp1$RAWCOLOUR:"Temp" \
LINE2:humid1$RAWCOLOUR2:"Humidity" \
COMMENT:" \\n" \
GPRINT:temp1:MAX:"Temp Max - %8.1lf%sc" \
COMMENT:" \\n" \
GPRINT:temp1:MIN:"Temp Min - %8.1lf%sc" \
COMMENT:" \\n" \
GPRINT:humid1:MAX:"Humidity Max - %4.1lf%s%%" \
COMMENT:" \\n" \
GPRINT:humid1:MIN:"Humidity Min - %4.1lf%s%%" \
COMMENT:" \\n" \
COMMENT:" \\n" \
COMMENT:"Created at $now_formatted"

#week
rrdtool graph $IMGPATH/week.png --start -7d \
--full-size-mode \
--width=700 --height=400 \
--slope-mode \
--color=SHADEB#9999CC \
--title="Garage Climate Week" \
--watermark="Garage Climate" \
--vertical-label='Temp(°C) Humid(%)' \
--upper-limit=100 \
--lower-limit=0 \
DEF:temp1=$RRDPATH/$RRDFILE:temp:AVERAGE \
DEF:humid1=$RRDPATH/$RRDFILE:humid:AVERAGE \
VDEF:TempMin=temp1,MINIMUM \
VDEF:TempMax=temp1,MAXIMUM \
LINE1:temp1$RAWCOLOUR:"Temp" \
LINE2:humid1$RAWCOLOUR2:"Humidity" \
COMMENT:" \\n" \
GPRINT:temp1:MAX:"Temp Max - %8.1lf%sc" \
COMMENT:" \\n" \
GPRINT:temp1:MIN:"Temp Min - %8.1lf%sc" \
COMMENT:" \\n" \
GPRINT:humid1:MAX:"Humidity Max - %4.1lf%s%%" \
COMMENT:" \\n" \
GPRINT:humid1:MIN:"Humidity Min - %4.1lf%s%%" \
COMMENT:" \\n" \
COMMENT:" \\n" \
COMMENT:"Created at $now_formatted"



#month
rrdtool graph $IMGPATH/month.png --start -1m \
--full-size-mode \
--width=700 --height=400 \
--slope-mode \
--color=SHADEB#9999CC \
--title="Garage Climate Month" \
--watermark="Garage Climate" \
--vertical-label='Temp(°C) Humid(%)' \
--upper-limit=100 \
--lower-limit=0 \
DEF:temp1=$RRDPATH/$RRDFILE:temp:AVERAGE \
DEF:humid1=$RRDPATH/$RRDFILE:humid:AVERAGE \
VDEF:TempMin=temp1,MINIMUM \
VDEF:TempMax=temp1,MAXIMUM \
LINE1:temp1$RAWCOLOUR:"Temp" \
LINE2:humid1$RAWCOLOUR2:"Humidity" \
COMMENT:" \\n" \
GPRINT:temp1:MAX:"Temp Max - %8.1lf%sc" \
COMMENT:" \\n" \
GPRINT:temp1:MIN:"Temp Min - %8.1lf%sc" \
COMMENT:" \\n" \
GPRINT:humid1:MAX:"Humidity Max - %4.1lf%s%%" \
COMMENT:" \\n" \
GPRINT:humid1:MIN:"Humidity Min - %4.1lf%s%%" \
COMMENT:" \\n" \
COMMENT:" \\n" \
COMMENT:"Created at $now_formatted"
root@alarmpi:/home/pi/scripts# 
