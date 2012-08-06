#coding=utf-8
from django.conf.urls.defaults import patterns

urlpatterns = patterns('main.views.message',
    (r'^$', 'message'),
    (r'^message_list/$', 'message_list'),
    (r'^message_dialog/(?P<case_id>\d+)/(?P<is_sys>\w+)/(?P<message_id>\d+)/$', 'message_dialog'),
    (r'^send/$', 'send'),
)