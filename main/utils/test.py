from form_check import *
from django.utils.datetime_safe import datetime
from main.models.mri import *
ssn = '123'
schedules = Schedule.objects.filter(mri=1).filter(date__gte=datetime.today())
print schedules