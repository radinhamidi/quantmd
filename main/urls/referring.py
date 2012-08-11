#coding=utf-8
from django.conf.urls.defaults import patterns

urlpatterns = patterns('main.views',
    (r'^dashboard/$', 'referring.dashboard'),
    (r'^patientsView/$', 'patients.patients_view'), #
    (r'^patientsInfo/$', 'patients.patientsList'), #
    (r'^patientInfo/(?P<patient_id>\d+)/$', 'patients.patientInfo'), #
    (r'^createPatient/$', 'patients.createView'), #
    (r'^createPatientAction/$', 'patients.createPatient'), #
    (r'^appointmentsInfo/(?P<patient_id>\d+)/$', 'appointment.appointment_view'),
    (r'^appointmentsSearch/(?P<patient_id>\d+)/$', 'appointment.appointment_search'),
    (r'^mriInfo/(?P<mri_id>\d+)/$', 'appointment.mri_info'),
    (r'^makeAppointment/$', 'appointment.make_appointment'),
    (r'^patientCase/(?P<case_id>\d+)/$', 'patients.patient_case'),
    (r'^view_mri_images/(?P<case_id>\d+)/$', 'patients.view_mri_images'),
    (r'^cancelAppointment/(?P<appointment_id>\d+)/$', 'appointment.appointment_cancel'),
    (r'^reschedule/(?P<appointment_id>\d+)/$', 'appointment.appointment_reschedule'),
    (r'^reappointmentSearch/(?P<appointment_id>\d+)/$', 'appointment.reappointment_search'),
    (r'^remakeAppointment/(?P<patient_id>\d+)/(?P<schedule_id>\d+)/(?P<appointment_id>\d+)/$', 'appointment.remake_appointment'),
    (r'^editPatientView/(?P<patient_id>\d+)/$', 'patients.patient_edit_view'),
    (r'^editPatientAction/(?P<patient_id>\d+)/$', 'patients.patient_edit_action'),
    (r'^viewAnalysis/(?P<case_id>\d+)/$', 'patients.view_analysis'),
    (r'^serviceSelect/(?P<patient_id>\d+)/(?P<schedule_id>\d+)/$', 'appointment.service_view'),
)