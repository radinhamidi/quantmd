from django.db import models

class Patient(models.Model):
    """
    Referring doctor will create patient record;
    Each patient can have only one record, uniquely identified by SSN 
    """
    ssn = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    gender = models.BooleanField(default=True) #1 for male, 0 for female
    birthday = models.DateField()
    email = models.EmailField()
    phone = models.IntegerField(max_length=20)
    address = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zip = models.IntegerField()
    
    class Meta: 
        app_label = 'main'

class PatientAndDoctor(models.Model):
    patient = models.ForeignKey('Patient')
    doctor = models.ForeignKey('Profile')
    
    class Meta: 
        app_label = 'main'
