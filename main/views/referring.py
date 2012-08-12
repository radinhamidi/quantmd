from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import *
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from main.models.account import *
from main.models.patient import *
from main.models.appointment import *
from main.models.case import *
from main.models.message import Message
import datetime
import operator
import time

def dashboard(request):
    msg_unread_count = Message.objects.filter(receiver__pk=request.user.pk, is_read = False, is_sys = False).count()
    diagnosis_unread_count = Message.objects.filter(receiver__pk=request.user.pk, is_read = False, is_sys = True, type = 4).count()
    reschedule_unread_count = Message.objects.filter(receiver__pk=request.user.pk, is_read = False, is_sys = True, type = 2).count()
    schedule_unread_count = Message.objects.filter(receiver__pk=request.user.pk, is_read = False, is_sys = True, type = 0).count()
    cancell_schedule_unread_count = Message.objects.filter(receiver__pk=request.user.pk, is_read = False, is_sys = True, type = 1).count()
    dicom_unread_count = Message.objects.filter(receiver__pk=request.user.pk, is_read = False, is_sys = True, type = 3).count()
    analysis_unread_count = Message.objects.filter(receiver__pk=request.user.pk, is_read = False, is_sys = True, type = 5).count()
    
    messages = Message.objects.filter(receiver__pk=request.user.pk, is_read = False).order_by('-create_time')
    
    doctor = Profile.objects.get(user = request.user)
    #Number of diagnosis with report for doctor to review
    return render_to_response('referring/dashboard.htm', {'messages': messages, 'msg':msg_unread_count, 'diagnosis':diagnosis_unread_count, 
                                                          'reschedule':reschedule_unread_count, 'schedule':schedule_unread_count, 
                                                          'cancelled':cancell_schedule_unread_count, 'dicom':dicom_unread_count, 'analysis': analysis_unread_count, 'doctor':doctor},
                                  context_instance=RequestContext(request))
