from django.db import models
from datetime import datetime

class Report(models.Model):
    content = models.TextField()
    create_time = models.DateTimeField(default=datetime.now)
    
    class Meta: 
        app_label = 'main'
        
class Meta: 
        app_label = 'main'