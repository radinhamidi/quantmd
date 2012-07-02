#coding=utf-8 
from django.contrib.auth.models import User as DjangoUser
from django.db import models

    
class Profile(models.Model):
    """Extends authorization module in Django"""  
    user = models.ForeignKey(DjangoUser, primary_key=True)
    name = models.CharField(max_length=200, db_index=True)
    bio = models.CharField(max_length=200, blank=True)
    gender = models.BooleanField(default=True)  #True(1) for male; False(0) for female
    
    def __unicode__(self):
        return self.name
    class Meta: 
        app_label = 'main'


class Organization(models.Model):
    """The site only opens to user with organization email specified here"""  
    name = models.CharField(max_length=100, db_index=True)
    domain = models.CharField(max_length=100, db_index=True)
    user_count = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.name
    class Meta: 
        app_label = 'main'

class EmailValidation(models.Model):
    user = models.ForeignKey(DjangoUser)
    email = models.CharField(max_length=75, unique=True)
    code = models.CharField(max_length=32)
    validated = models.BooleanField(default=False)
    class Meta: 
        app_label = 'main'
        
        
        