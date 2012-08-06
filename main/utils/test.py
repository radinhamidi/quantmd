import datetime
import time
str = '12:30'
date = datetime.datetime(int(2012),int(11),int(03))
today = datetime.datetime.now()
days = date - today
month = days.days/30
print month
