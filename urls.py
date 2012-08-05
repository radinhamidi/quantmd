#coding=utf-8 
from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    (r'^admin/', include(admin.site.urls)),
)

handler500 = 'main.views.error.server_error'

urlpatterns += patterns('main.views',
    (r'^$', 'index.index'),
    (r'^login/$', 'account.login_action'),
    (r'^logout/$', 'account.logout_view'),
    (r'^changePasswordView/$', 'account.change_password_view'),
    (r'^changePassword/$', 'account.change_password'),
    (r'^referring/', include('main.urls.referring')),
    (r'^receptionist/', include('main.urls.receptionist')),
    (r'^broker/', include('main.urls.broker')),
    (r'^cardiologist/', include('main.urls.cardiologist')),
    (r'^message/', include('main.urls.message')),
)
