'''
Created on Jul 6, 2012

@author: Young
'''
from django.db import models
class Patient(models.Model):
    ssn = models.IntegerField(max_length=200)
    birthDate = models.DateField()
    email = models.EmailField()
    phone = models.IntegerField(max_length=20)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zip = models.IntegerField(max_length=100)
    
    class Meta: 
        app_label = 'main'

class PatientAndDoctor(models.Model):
    patient = models.ForeignKey('Patient')
    doctor = models.ForeignKey('Profile')
    
    class Meta: 
        app_label = 'main'
