from models.account import Profile
from django.contrib import admin
from models.account import *
from models.case import *
from models.mri import *
from models.patient import *
from models.appointment import *
from models.report import *
from models.data import *
from models.message import *

admin.site.register(Profile)
admin.site.register(Appointment)
admin.site.register(Case)
admin.site.register(MRIData)
admin.site.register(Message)
admin.site.register(MRICenter)
admin.site.register(Schedule)
admin.site.register(Patient)
admin.site.register(PatientAndDoctor)
admin.site.register(Report)


