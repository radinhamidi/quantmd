from django.db import models
from account import Profile
from datetime import datetime

class Analysis(models.Model):
    """
    Store the uploaded files in dicom/{random_string}/analysis folder
    Admin won't be able to enter any text analysis
    """
    admin = models.ForeignKey(Profile)
    content = models.CharField(max_length=1000)
    create_time = models.DateTimeField(default=datetime.now)
    
    class Meta: 
        app_label = 'main'