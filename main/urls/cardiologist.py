#coding=utf-8
from django.conf.urls.defaults import patterns

urlpatterns = patterns('main.views.cardiologist',
    (r'^case/$', 'case'),
    (r'^accept_case/$', 'accept_case'),
    (r'^submit_report/$', 'submit_report'),
    (r'^logs/$', 'logs'),
    
    
)