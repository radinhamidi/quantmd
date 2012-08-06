from django.db import models
from account import Profile

class Patient(models.Model):
    """
    Referring doctor will create patient record;
    Each patient can have only one record, uniquely identified by ID
    """
    ssn = models.IntegerField()
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    gender = models.BooleanField(default=True) #1 for male, 0 for female
    birthday = models.DateField()
    email = models.EmailField()
    phone = models.BigIntegerField()
    address = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zip = models.IntegerField()
    doctor = models.ForeignKey(Profile)
    
    class Meta:
        app_label = 'main'
    def __unicode__(self):
        if self.middle_name:
            return self.first_name + ' ' + self.middle_name + ' ' + self.last_name
        else:
            return self.first_name + ' ' + self.last_name
