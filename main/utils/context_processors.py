#coding=utf-8
from django.conf import settings
    
def constants(request):
    dict = {}
    dict['APP_URL'] = settings.APP_URL
    return dict    
