from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import *
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from main.models.account import *
from main.models.patient import *
from main.models.appointment import *
from main.models.mri import *
from main.utils.form_check import *
from main.models.case import *
from main.models.data import *
from django.utils.datetime_safe import datetime

def message_list(request):
    print "aaaa"
    return render_to_response('referring/messages.htm', {},
                            context_instance=RequestContext(request))

def message_info(request, message_id):
    return render_to_response('referring/individual-message.htm', {},
                            context_instance=RequestContext(request))
