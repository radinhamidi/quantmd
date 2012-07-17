from django.db import models
from account import Profile
from case import Case

class Message(models.Model):
    sender = models.ForeignKey(Profile, related_name='Message_sender')
    receiver = models.ForeignKey(Profile, related_name='Message_receiver')
    case = models.ForeignKey(Case)
    content = models.CharField(max_length=3000)
    is_read = models.BooleanField(default=False) #Is it read by receiver?
    deleted_by_receiver = models.BooleanField(default=False)
    deleted_by_sender = models.BooleanField(default=False)
    create_time = models.DateField()
     
    class Meta: 
        app_label = 'main'