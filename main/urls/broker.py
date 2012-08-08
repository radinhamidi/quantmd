#coding=utf-8
from django.conf.urls.defaults import patterns

urlpatterns = patterns('main.views.broker',
    (r'^patients/$', 'patients'),
    (r'^upload/(?P<patient_id>\d+)/(?P<case_id>\d+)/$', 'upload'),
    (r'^upload_action/$', 'upload_action'),
    (r'^upload_complete/$', 'upload_complete'),
    (r'^logs/$', 'logs'),
)