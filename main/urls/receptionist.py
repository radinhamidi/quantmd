#coding=utf-8
from django.conf.urls.defaults import patterns

urlpatterns = patterns('main.views.receptionist',
    (r'^registerList/$', 'register_list'),
    (r'^register/(?P<appointment_id>\d+)/$', 'register'),
    (r'^checkIn/(?P<appointment_id>\d+)/$', 'check_in'),
    (r'^cancel/(?P<appointment_id>\d+)/$', 'cancel'),
    (r'^cancelSchedule/(?P<schedule_id>\d+)/$', 'cancel_schedule'),
    (r'^scheduleList/$', 'schedule_list_view'),
    (r'^timeslotList/$', 'timeslot_list'),
    (r'^logs/$', 'logs'),
    (r'^registerCancellation/(?P<appointment_id>\d+)/$', 'cancel_register'),
    (r'^registered_view/(?P<appointment_id>\d+)/$', 'register_cancellation_view'),
)