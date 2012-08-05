from django.db import models
from account import Profile
from case import Case
from datetime import datetime

class Message(models.Model):
    receiver = models.ForeignKey(Profile)
    case = models.ForeignKey(Case)
    title = models.CharField(max_length=1000)
    content = models.CharField(max_length=3000)
    is_read = models.BooleanField(default=False)#Is it read by receiver?
    #0 for appointment confirm, 1 for appointment cancel, 2 for reschedule, 3 for diagnosis available
    type = models.SmallIntegerField()
    create_time = models.DateField(default=datetime.now)
     
    class Meta: 
        app_label = 'main'


class Chat(models.Model):
    sender = models.ForeignKey(Profile, related_name='Message_sender')
    receiver = models.ForeignKey(Profile, related_name='Message_receiver')
    case = models.ForeignKey(Case)
    content = models.CharField(max_length=3000)
    is_read = models.BooleanField(default=False) #Is it read by receiver?
    create_time = models.DateField(default=datetime.now)
    
    class Meta: 
        app_label = 'main'