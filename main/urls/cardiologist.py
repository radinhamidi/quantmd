#coding=utf-8
from django.conf.urls.defaults import patterns

urlpatterns = patterns('main.views.cardiologist',
    (r'^acceptCaseView/$', 'accept_case_view'),
    (r'^acceptAction/$', 'accept_case_action'),
    (r'^caseView/$', 'case_view'),
    (r'^viewReport/$', 'view_report'),
    (r'^handinReport/(?P<case_id>\d+)/$', 'handin_report'),
    (r'^casesList/$', 'diagnosis_list'),
)