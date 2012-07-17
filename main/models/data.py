from django.db import models
from account import Profile
from datetime import datetime

class MRIData(models.Model):
    """
    Information about the dicom file
    """
    broker = models.ForeignKey(Profile)
    file = models.CharField(max_length=200)
    create_time = models.DateTimeField(default=datetime.now)
    
    class Meta: 
        app_label = 'main'