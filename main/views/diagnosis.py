from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import *
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from main.models.mri import *
from main.models.appointment import *
from main.models.patient import *
from main.models.account import *
from django.utils.datetime_safe import datetime
from main.models.case import *
from main.models.report import *


def diagnosis_lsit(request):
    print "diagnosis"
    if request.user.is_authenticated():
        doctor = request.user
        appointments = Appointment.objects.filter(doctor=doctor)
        print "here1" 
        cases = {}
        for appointment in appointments:
            patient = appointment.patient
            case = Case.objects.get(appointment = appointment)
            if case.report is not None:
                cases[case.report] = patient
        print cases   
        return render_to_response('referring/diagnosis.htm', {'cases':cases},
                              context_instance=RequestContext(request))
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
def diagnosis_view(request, report_id):
    print "cc"
    if request.user.is_authenticated():
        report = Report.objects.get(id=report_id)
        case = Case.objects.get(report=report)
        appointment = case.appointment
        patient = appointment.patient
        mri = appointment.mri
        print report                
        return render_to_response('referring/individual-diagnosis.htm', {'report':report, 'patient':patient, 'mri':mri},
                            context_instance=RequestContext(request))
    
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))    