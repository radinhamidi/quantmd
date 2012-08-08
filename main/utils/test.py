import datetime
import time
schedule_date = '06/08/1988'
format="%m/%d/%Y"
date = datetime.datetime.strptime(schedule_date,format)

print date.date() < datetime.datetime.now().date()
