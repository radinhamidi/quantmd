'''
Created on Jul 6, 2012

@author: Young
'''
from django.db import models
class Appointment(models.Model):
    referringDoc = models.ForeignKey('User')
    schedule = models.ForeignKey('Schedule')
    patient = models.ForeignKey('Patient')
    
    class Meta: 
        app_label = 'main'
        
class Service(models.Model):
    description = models.CharField(max_length = 200)
    name = models.CharField(max_length = 200)
    provider = models.CharField(max_length = 200)
    type = models.IntegerField(max_length = 1)
    
    class Meta:
        app_label = 'main'
        
class ServiceAppoint(models.Model):
    appointment = models.ForeignKey('Appointment')
    service = models.ForeignKey('Service')
    
    class Meta: 
        app_label = 'main'