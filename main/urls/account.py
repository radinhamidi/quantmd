#coding=utf-8
from django.conf.urls.defaults import patterns

urlpatterns = patterns('main.views',
    (r'^login/$', 'account.login_action'),
    (r'^login_action/$', 'account.login_action'),
    (r'^logout/$', 'account.logout_view'),
)