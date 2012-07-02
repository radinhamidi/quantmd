from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from main.models.account import *

def index(request):
    if not request.user.is_authenticated():
        orgs = Organization.objects.all()
        return render_to_response('main/account/login.html', {'orgs':orgs},
                              context_instance=RequestContext(request))
    
    return render_to_response('main/index.html',{}, context_instance=RequestContext(request))
    
    