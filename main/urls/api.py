#coding=utf-8
from django.conf.urls.defaults import patterns

urlpatterns = patterns('main.views.api',
    (r'^dicom_zip/(?P<case_id>\d+)/$', 'dicom_zip'),
    (r'^upload_analysis/(?P<case_id>\d+)/(?P<admin_id>\d+)/$', 'upload_analysis'),
    (r'^get_schedule_by_day/(?P<mri_id>\d+)/(?P<date_str>\d+-\d+-\d+)/$', 'get_schedule_by_day'),
    (r'^add_slot/(?P<mri_id>\d+)/(?P<date_str>\d+-\d+-\d+)/(?P<time_str>\d+:\d+:\d+)/$', 'add_slot'),
    
)