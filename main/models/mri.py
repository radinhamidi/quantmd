'''
Created on Jul 6, 2012

@author: Young
'''
from django.db import models
class MriCenter(models.Model):
    email = models.EmailField()
    phone = models.IntegerField(max_length=30)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zip = models.IntegerField(max_length=100)
    longitude = models.CharField(max_length=20)
    latitude = models.CharField(max_length=20)
    
    class Meta: 
        app_label = 'main'
        
class Schedule(models.Model):
    date = models.DateField()
    startTime = models.TimeField()
    endTime = models.TimeField()
    isAvailible = models.BooleanField(default=False)
    class Meta: 
        app_label = 'main'
    
class MriData(models.Model):
    file = models.FilePathField()
    uploadDate = models.DateField()
    mriUser = models.ForeignKey('User')
    
    class Meta: 
        app_label = 'main'
    