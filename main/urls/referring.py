#coding=utf-8
from django.conf.urls.defaults import patterns

urlpatterns = patterns('main.views',
    (r'^patientsInfo/$', 'patients.patientsList'),
    (r'^patientInfo/(?P<patient_ssn>\d+)/$', 'patients.patientInfo'),
    (r'^createPatient/$', 'patients.createView'),
    (r'^createPatientAction/$', 'patients.createPatient'),
    (r'^appointmentsInfo/$', 'appointment.appointment_view'),
    (r'^appointmentsSearch/$', 'appointment.appointment_search'),
)