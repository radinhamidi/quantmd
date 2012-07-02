#coding=utf-8
from django.conf.urls.defaults import patterns

urlpatterns = patterns('main.views',
    (r'^login/$', 'account.login_view'),
    (r'^login_action/$', 'account.login_action'),
    (r'^logout/$', 'account.logout_view'),
    (r'^register_action/$', 'account.register_action'),
    (r'^validate_email/(?P<code>[\w\W]+)/$', 'account.validate_email'),
)