#coding=utf-8
from django.conf.urls.defaults import patterns

urlpatterns = patterns('main.views.quantmd',
    (r'^cardiologist/$', 'cardiologist'),
    
    
    #Yang Xie's url below this line
    (r'^mri/$', 'mri'),
    (r'^createMRI/$', 'create_mri_action'),
    (r'^createMRIView/$', 'create_mri_view'),
)