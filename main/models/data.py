from django.db import models
from account import Profile
from datetime import datetime
from case import Case

class MRIData(models.Model):
    """
    Information about the dicom file
    """
    broker = models.ForeignKey(Profile)
    file = models.CharField(max_length=200)
    create_time = models.DateTimeField(default=datetime.now)
    case = models.ForeignKey(Case)
    class Meta: 
        app_label = 'main'
        
        
        
class Image(models.Model):
    
    data = models.ForeignKey(MRIData)
    image = models.CharField(max_length=200)
    
    class Meta: 
        app_label = 'main'