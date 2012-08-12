import datetime
import time
def get_monday():
    today = datetime.datetime.now()
    w = today.weekday()
    monday = today - datetime.timedelta(days=w)
    tmp = monday.strftime('%Y%m%d')
    monday = datetime.datetime(int(tmp[:4]), int(tmp[4:6]), int(tmp[6:]))

    return monday
