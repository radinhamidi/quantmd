#coding=utf-8 
from django.db import models

    
class User(models.Model):
    name = models.CharField(max_length=200,unique=True)
    password = models.CharField(max_length=200)
    role = models.IntegerField(max_length=1)
    profileId = models.ForeignKey('Profile')
   
    class Meta: 
        app_label = 'main'
    
class Profile(models.Model):
    name = models.CharField(max_length=200)
    gender = models.IntegerField(max_length=1)
    email = models.EmailField()
    phone = models.IntegerField(max_length=30)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zip = models.IntegerField(max_length=20)
    mriId = models.ForeignKey('MriCenter')
    
    class Meta: 
        app_label = 'main'
        
class Message(models.Model):
    sender = models.ForeignKey('User', related_name='Message_sender')
    receiver = models.ForeignKey('User',related_name='Message_receiver')
    content = models.CharField(max_length=200)
    date = models.DateField()
    isRead = models.BooleanField(default = False)
     
    class Meta: 
        app_label = 'main'