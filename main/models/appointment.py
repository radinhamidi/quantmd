from django.db import models
from account import Profile
from mri import Schedule, MRICenter
from patient import Patient
from case import Case
from datetime import datetime

class Appointment(models.Model):
    """
    The appointment to take MRI scan at MRI center
    It can only be created by referring doctor
    It can be cancelled by either doctor or MRI center
    The schedule can be changed by both doctor and MRI center
    """
    doctor = models.ForeignKey(Profile) #The referring doctor
    patient = models.ForeignKey(Patient)
    schedule = models.ForeignKey(Schedule)
    mri = models.ForeignKey(MRICenter)
    case = models.ForeignKey(Case)
    case_status = models.SmallIntegerField(default=0) #replicated from Case model
    is_current = models.BooleanField(default=True) #Is the appointment for current case 
    is_cancelled = models.BooleanField(default=False)
    create_time = models.DateTimeField(default=datetime.now)
    cancelled_by_doctor = models.BooleanField(default=True) #otherwise, cancelled by mri center
    is_check_in = models.BooleanField(default=False)
    check_in_time = models.DateTimeField(blank=True, null=True)
    is_check_out = models.BooleanField(default=False)
    check_out_time = models.DateTimeField(blank=True, null=True)
    
    class Meta: 
        app_label = 'main'
        

        
#class Service(models.Model):
#    description = models.CharField(max_length = 200)
#    name = models.CharField(max_length = 200)
#    provider = models.CharField(max_length = 200)
#    type = models.IntegerField(max_length = 1)
#    
#    class Meta:
#        app_label = 'main'
#        
#class ServiceAppoint(models.Model):
#    appointment = models.ForeignKey('Appointment')
#    service = models.ForeignKey('Service')
#    
#    class Meta: 
#        app_label = 'main'