#coding=utf-8
from django.conf.urls.defaults import patterns

urlpatterns = patterns('main.views.broker',
    (r'^upload/$', 'upload'),
    (r'^upload_action/$', 'upload_action'),
    
)