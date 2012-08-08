from django.db import models
from account import Profile
from case import Case
from datetime import datetime


class Message(models.Model):
    is_sys = models.BooleanField(default=False)
    #0 for appointment confirm, 1 for appointment cancel, 2 for reschedule, 
    #3, Dicom file uploaded 4 for diagnosis available 5 for quantmd analysis available
    type = models.SmallIntegerField(default=-1) #only used by system message
    
    sender = models.ForeignKey(Profile, null=True, blank=True, related_name="msg_sender")
    receiver = models.ForeignKey(Profile, related_name="msg_receiver")
    case = models.ForeignKey(Case)
    title = models.CharField(max_length=200, blank=True)
    content = models.CharField(max_length=3000)
    is_read = models.BooleanField(default=False)#Is it read by receiver?
    create_time = models.DateTimeField(default=datetime.now)
    
    class Meta: 
        app_label = 'main'
