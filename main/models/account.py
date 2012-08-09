#coding=utf-8 
from django.db import models
from django.contrib.auth.models import User
from mri import MRICenter
    
class Profile(models.Model):
    user = models.ForeignKey(User, primary_key=True)
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20)
    gender = models.BooleanField(default=True) #1 for male, 0 for female
    email = models.EmailField()
    phone = models.BigIntegerField()
    address = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zip = models.IntegerField()
    
    #0 for quantmd backend, 1 for doctor, 2 for register(receptionist), 3 for broker, 4 for cardiologist
    role = models.SmallIntegerField(default=0)
    #Each register and broker is associated with a MRI center
    mri_id = models.ForeignKey(MRICenter, blank=True, null=True) 
    
    class Meta: 
        app_label = 'main'
    def __unicode__(self):
        return self.first_name + ' ' + self.last_name
