#coding=utf-8 
from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}), 
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}), 
    (r'^robots\.txt$', direct_to_template,{'template': 'robots.txt', 'mimetype': 'text/plain'}),
     
    (r'^admin/', include(admin.site.urls)),
)

handler500 = 'main.views.error.server_error'

urlpatterns += patterns('main.views',
    (r'^$','index.index'),
    (r'^privacy$','misc.privacy'),
    (r'^tos$','misc.tos'),
    (r'^account/',include('main.urls.account')),
    
    
)
