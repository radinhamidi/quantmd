#coding=utf-8
from django.conf.urls.defaults import patterns

urlpatterns = patterns('main.views.api',
    (r'^dicom_zip/(?P<case_id>\d+)/$', 'dicom_zip'),
)