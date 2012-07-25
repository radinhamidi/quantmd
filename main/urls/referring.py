#coding=utf-8
from django.conf.urls.defaults import patterns

urlpatterns = patterns('main.views',
    (r'^patientsInfo/$', 'patients.patientsList'),
    (r'^patientInfo/(?P<patient_ssn>\d+)/$', 'patients.patientInfo'),
    (r'^createPatient/$', 'patients.createView'),
    (r'^patientSSNCheck/$', 'patients.check_ssn'),
    (r'^patientSSNlink/$', 'patients.ssn_link'),
    (r'^createPatientAction/$', 'patients.createPatient'),
    (r'^appointmentsInfo/$', 'appointment.appointment_view'),
    (r'^appointmentsSearch/$', 'appointment.appointment_search'),
    (r'^mriInfo/(?P<mri_id>\d+)/$', 'appointment.mri_info'),
    (r'^mriSchedule/(?P<mri_id>\d+)/$', 'appointment.mri_schedule'),
    (r'^scheduleDetail/(?P<schedule_id>\d+)/$', 'appointment.schedule_detail'),
    (r'^makeAppointment/(?P<schedule_id>\d+)/$', 'appointment.make_appointment'),
    (r'^patientAppointmentList/(?P<patient_ssn>\d+)/$', 'patients.patient_appotiments'),
    (r'^patientAppointment/(?P<schedule_id>\d+)/(?P<patient_ssn>\d+)/$', 'patients.patient_appotiment'),
    (r'^patientCaseList/(?P<patient_ssn>\d+)/$', 'patients.patient_cases'),
    (r'^patientCase/(?P<case_id>\d+)/$', 'patients.patient_case'),
    (r'^diagnosisesInfo/$', 'diagnosis.diagnosis_lsit'),
    (r'^dignosisView/(?P<report_id>\d+)/$', 'diagnosis.diagnosis_view'),
    (r'^cancelAppointment/(?P<appointment_id>\d+)/$', 'appointment.appointment_cancel'),
)