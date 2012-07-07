'''
Created on Jul 6, 2012

@author: Young
'''
from django.db import models

class Case(models.Model):
    appointment = models.ForeignKey('Appointment')
    data = models.ForeignKey('MriData')
    report = models.ForeignKey('Report')
    cardiologists = models.ForeignKey('User')
    createTime = models.DateField()
    
    class Meta: 
        app_label = 'main'
        
class Report(models.Model):
    content = models.TextField()
    date = models.DateField()
    
    class Meta: 
        app_label = 'main'