import datetime
import time
today = datetime.datetime.now()
today = datetime.datetime.now()
w = today.weekday()
sunday = today - datetime.timedelta(days=w)
tmp = sunday.strftime('%Y%m%d')
sunday = datetime.datetime(int(tmp[:4]), int(tmp[4:6]), int(tmp[6:]))

print sunday
