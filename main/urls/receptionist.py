#coding=utf-8
from django.conf.urls.defaults import patterns

urlpatterns = patterns('main.views.receptionist',
    (r'^registerList/$', 'register_list'),
    (r'^checkInCancell/(?P<appointment_id>\d+)/$', 'check_in_cancell'),
    (r'^checkIn/(?P<appointment_id>\d+)/$', 'check_in'),
    (r'^checkOut/(?P<appointment_id>\d+)/$', 'check_out'),
    (r'^cancel/(?P<appointment_id>\d+)/$', 'cancel'),
    (r'^cancelSchedule/(?P<schedule_id>\d+)/$', 'cancel_schedule'),
    (r'^scheduleList/(?P<month>\d+)/(?P<negative>\d+)/$', 'schedule_list_view'),
    (r'^amendTimesolt/(?P<month>\d+)/(?P<negative>\d+)/$', 'amend_timesolt'),
    (r'^rescheduleList/$', 'reschedule_list_view'),
    (r'^reschedule/(?P<appointment_id>\d+)/$', 'reschedule_view'),
    (r'^rescheduleAction/(?P<schedule_id>\d+)/$', 'reschedule_action'),
    (r'^timeslotList/$', 'timeslot_list'),
    (r'^logs/$', 'logs'),
    (r'^registerCancellation/(?P<appointment_id>\d+)/$', 'cancel_register'),
    (r'^registered_view/(?P<appointment_id>\d+)/$', 'register_cancellation_view'),
)