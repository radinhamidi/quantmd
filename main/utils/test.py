import datetime

today = datetime.datetime.now()
month = 1
today = today + datetime.timedelta(months = int(month))
print today