#coding=utf-8
from django.conf.urls.defaults import patterns

urlpatterns = patterns('main.views',
    (r'^registerList/$', 'receptionist.register_list'),
    (r'^register/(?P<appointment_id>\d+)/$', 'receptionist.register'),
    (r'^checkIn/(?P<appointment_id>\d+)/$', 'receptionist.check_in'),
    (r'^cancel/(?P<appointment_id>\d+)/$', 'receptionist.cancel'),
    (r'^cancelSchedule/(?P<schedule_id>\d+)/$', 'receptionist.cancel_schedule'),
    (r'^scheduleList/$', 'receptionist.schedule_list_view'),
    (r'^timeslotList/$', 'receptionist.timeslot_list'),
)