#coding=utf-8
from django.conf.urls.defaults import patterns

urlpatterns = patterns('main.views.quantmd',
    (r'^create_user/(?P<role>[-]?\d+)/$', 'create_user'),
    (r'^create_user_action/$', 'create_user_action'),
    (r'^edit_user/(?P<user_id>\d+)/$', 'edit_user'),
    (r'^edit_user_action/$', 'edit_user_action'),
    (r'^view_user/(?P<user_id>\d+)/$', 'view_user'),
    (r'^doctors/$', 'doctors'),
    (r'^receptionists/$', 'receptionists'),
    (r'^brokers/$', 'brokers'),
    (r'^cardiologists/$', 'cardiologists'),
    (r'^process_cases/$', 'process_cases'),
    (r'^process_case/(?P<case_id>\d+)/$', 'process_case'),
    (r'^upload_action/$', 'upload_action'),
    (r'^process_case_action/$', 'process_case_action'),
    
    
    #Yang Xie's url below this line
    (r'^mri/$', 'mri'),
    (r'^createMRI/$', 'create_mri_action'),
    (r'^editMRIView/(?P<mri_id>\d+)/$', 'edit_mri_view'),
    (r'^MRIView/(?P<mri_id>\d+)/$', 'mri_view'),
    (r'^scheduleList/(?P<mri_id>\d+)/(?P<month>-?\d+)/$', 'mri_schedule'),
    (r'^editMRIAction/$', 'edit_mri_action'),
    (r'^createMRIView/$', 'create_mri_view'),
    (r'^logsView/$', 'logs_view'),
    (r'^logView/(?P<case_id>\d+)/$', 'log_view'),
    (r'^dashboard/$', 'dashborad'),
    (r'^servicesView/$', 'services_view'),
    (r'^stopService/(?P<service_id>\d+)/$', 'services_stop'),
    (r'^activeService/(?P<service_id>\d+)/$', 'services_active'),
    (r'^addService/$', 'services_add'),
)