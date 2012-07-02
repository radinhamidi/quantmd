#coding=utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext

    
def privacy(request):
    return render_to_response('main/misc/privacy.html', {},
                              context_instance=RequestContext(request))

def tos(request):
    return render_to_response('main/misc/tos.html', {},
                          context_instance=RequestContext(request))
  
