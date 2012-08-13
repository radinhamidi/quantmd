from django.db import models
from account import Profile
from datetime import datetime


class MRIData(models.Model):
    """
    Information about the dicom file, the report and admin uploaded file
    There will be a subfolder named 'analysis' that contains the analysis
    files uploaded by quantmd admin 
    """
    broker = models.ForeignKey(Profile)
    name = models.CharField(max_length=200) #The name used for folder, dicom file and images
    image_count = models.IntegerField(default=0) #Total number of images of different sequences
    create_time = models.DateTimeField(default=datetime.now)
    class Meta: 
        app_label = 'main'

class Comment(models.Model):
    data = models.ForeignKey(MRIData)
    image_index = models.IntegerField(default=0)
    content = models.CharField(max_length=1000)
    class Meta: 
        app_label = 'main'
    

        