from django.db import models
from account import Profile
from datetime import datetime

class Analysis(models.Model):
    admin = models.ForeignKey(Profile)
    content = models.TextField()
    create_time = models.DateTimeField(default=datetime.now)
    
    class Meta: 
        app_label = 'main'