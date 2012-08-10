#coding=utf-8
from django.conf.urls.defaults import patterns

urlpatterns = patterns('main.views.quantmd',
    (r'^create_user/$', 'create_user'),
    (r'^create_user_action/$', 'create_user_action'),
    (r'^edit_user/(?P<user_id>\d+)/$', 'edit_user'),
    (r'^view_user/(?P<user_id>\d+)/$', 'view_user'),
    (r'^doctors/$', 'doctors'),
    (r'^receptionists/$', 'receptionists'),
    (r'^brokers/$', 'brokers'),
    (r'^cardiologists/$', 'cardiologists'),
    
    
    
    #Yang Xie's url below this line
    (r'^mri/$', 'mri'),
    (r'^createMRI/$', 'create_mri_action'),
    (r'^createMRIView/$', 'create_mri_view'),
    (r'^logsView/$', 'logs_view'),
    (r'^logView/(?P<case_id>\d+)/$', 'log_view'),
)