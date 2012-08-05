from django.db import models
from datetime import datetime

class MRICenter(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.BigIntegerField()
    address = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200,blank=True)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zip = models.IntegerField(default=0)
    longitude = models.FloatField(default=0)
    latitude = models.FloatField(default=0)
    
    class Meta: 
        app_label = 'main'
        
class Schedule(models.Model):
    """
    The schedule is stored for all slots; Each slots is 30 minutes wide, enough for a scan
    A slot is available only if MRI center sets so. 
    If MRI center finds it unavailable, it deletes the record 
    Once booked, the record is changed to unavailable but not removed 
    """
    mri = models.ForeignKey(MRICenter)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    is_cancelled = models.BooleanField(default=False)
    
    class Meta: 
        app_label = 'main'
    

    