from django.db import models
from datetime import datetime

class Report(models.Model):
    content = models.TextField()
    pdf_file = models.CharField(max_length=200, null=True) #PDF file path starts with dicom/
    create_time = models.DateTimeField(default=datetime.now)
    
    class Meta:
        app_label = 'main'
        
