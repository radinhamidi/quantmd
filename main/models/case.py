from django.db import models
from account import Profile
from report import Report
from datetime import datetime
from data import MRIData
from patient import Patient
from analysis import Analysis

class Service(models.Model):
    """
    The services list the MRI center provide
    """
    name = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    
    class Meta: 
        app_label = 'main'
        
        
class Case(models.Model):
    """
    A case encapsulates the whole process from doctor to 
    mri center to cardiologist
    A case is automatically created when an appointment is scheduled;
    If the appointment is cancelled, it's status set to -1 in case;
    """
    patient = models.ForeignKey(Patient)
    data = models.ForeignKey(MRIData,blank=True, null=True)
    analysis = models.ForeignKey(Analysis, blank=True, null=True)
    report = models.ForeignKey(Report,blank=True, null=True)
    cardiologist = models.ForeignKey(Profile,blank=True, null=True)
    create_time = models.DateTimeField(default=datetime.now)
    #the time of the cardiologist assigned to the case
    assigned_time = models.DateTimeField(blank=True, null=True)
    # -1 for appointment and case cancelled, 0 for appointment created, 1 for checked in,
    #2 for broker uploaded, 3 for quantmd analysis finished, 4 for cardiologist assigned, 
    #5 for report uploaded, 6 for doctor have read the report
    status = models.SmallIntegerField(default=0) #should be replicated to Appointment model
    services = models.ManyToManyField(Service, through='ServiceAndCase')
    
    class Meta: 
        app_label = 'main'
        

        
class ServiceAndCase(models.Model):
    """The service that a case needs"""
    service = models.ForeignKey(Service)
    case = models.ForeignKey(Case)
    
    class Meta: 
        app_label = 'main'

