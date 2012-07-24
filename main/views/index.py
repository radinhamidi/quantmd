from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from main.models.account import *

def index(request):
    if not request.user.is_authenticated():
        return render_to_response('login.htm', {},
                              context_instance=RequestContext(request))
    
    profile = Profile.objects.get(pk=request.user.pk)
    if profile.role == 1:
        return render_to_response('referring/index.htm', {'Profile':profile},
                                  context_instance=RequestContext(request))
    elif profile.role == 2:
        return render_to_response('receptionist/index.htm', {'Profile':profile},
                                  context_instance=RequestContext(request))
    elif profile.role == 3:
        return render_to_response('broker/index.htm', {'Profile':profile},
                                  context_instance=RequestContext(request))
    elif profile.role == 4:
        return render_to_response('cardiologist/index.htm', {'Profile':profile},
                                  context_instance=RequestContext(request))
    elif profile.role == 0:
        return render_to_response('quantmd/index.htm', {'Profile':profile},
                                  context_instance=RequestContext(request))
    
    