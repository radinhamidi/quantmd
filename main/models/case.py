from django.db import models
from account import Profile
from mri import Schedule, MRICenter
from data import MRIData
from patient import Patient
from appointment import Appointment
from report import Report
from datetime import datetime


class Case(models.Model):
    """
    A case encapsulates the whole process from doctor to 
    mri center to cardiologist
    A case is automatically created when an appointment is scheduled;
    If the appointment is cancelled, it's set to null in case;
    """
    appointment = models.ForeignKey(Appointment)
    data = models.ForeignKey(MRIData, blank=True, null=True)
    report = models.ForeignKey(Report,blank=True, null=True)
    cardiologist = models.ForeignKey(Profile,blank=True, null=True)
    createTime = models.DateTimeField(default=datetime.now)
    #0 for appointment created, -1 for appointment cancelled, 1 for MRI scan complete, 
    #2 for broker uploaded, 3 for report uploaded, 4 for doctor have read the report
    status = models.SmallIntegerField(default=0)
    
    class Meta: 
        app_label = 'main'
        
