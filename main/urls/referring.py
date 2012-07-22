#coding=utf-8
from django.conf.urls.defaults import patterns

urlpatterns = patterns('main.views',
    (r'^patientsInfo/$', 'patients.patientsList'),
    (r'^patientInfo/(?P<patient_ssn>\d+)/$', 'patients.patientInfo'),
    (r'^createPatient/$', 'patients.createView'),
    (r'^createPatientAction/$', 'patients.createPatient'),
    (r'^appointmentsInfo/$', 'appointment.appointment_view'),
    (r'^appointmentsSearch/$', 'appointment.appointment_search'),
    (r'^mriInfo/(?P<mri_id>\d+)/$', 'appointment.mri_info'),
    (r'^mriSchedule/(?P<mri_id>\d+)/$', 'appointment.mri_schedule'),
    (r'^scheduleDetail/(?P<schedule_id>\d+)/$', 'appointment.schedule_detail'),
    (r'^makeAppointment/(?P<schedule_id>\d+)/$', 'appointment.make_appointment'),
)