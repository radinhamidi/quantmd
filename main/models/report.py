from django.db import models
from datetime import datetime

class Report(models.Model):
    content = models.TextField()
    report_file = models.CharField(max_length=200, null=True) #PDF file
    create_time = models.DateTimeField(default=datetime.now)
    
    class Meta:
        app_label = 'main'
        
