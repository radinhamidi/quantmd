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
from django.utils.datetime_safe import datetime

def dashboard(request):
    msg_unread_count = Message.objects.filter(receiver__pk=request.user.pk).count()
    #Number of diagnosis with report for doctor to review
    diagnosis_count = Appointment.objects.filter(doctor__pk=request.user.pk, case__status=5).count()
    patients_scheduled_count =  Appointment.objects.filter(doctor__pk=request.user.pk, case__status=5).count()
    return render_to_response('referring/dashboard.htm', {},
                                  context_instance=RequestContext(request))