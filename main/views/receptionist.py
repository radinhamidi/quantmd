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


def register_list(request):
    if request.user.is_authenticated():
        print "here"
        profile = Profile.objects.get(user = request.user)
        appointments = Appointment.objects.filter(mri=profile.mri_id).filter(is_check_in = False)
        print appointments
        return render_to_response('receptionist/register.htm',{'appointments':appointments}, context_instance=RequestContext(request))  
    else: 
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
def register(request, appointment_id):
    if request.user.is_authenticated():
        if Appointment.objects.filter(id=appointment_id).exists():
            appointment = Appointment.objects.get(id=appointment_id)
            patient = appointment.patient
            age = datetime.now().year - patient.birthday.year
            print appointment
            return render_to_response('receptionist/registration-confirmation.htm',{'appointment':appointment, 'age':age}, context_instance=RequestContext(request))
        else:
            return render_to_response('receptionist/error.htm',{'error':"error"}, context_instance=RequestContext(request))
    else: 
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
def check_in(request, appointment_id):
    print "here"
    if request.user.is_authenticated():
        if Appointment.objects.filter(id=appointment_id).exists():
            appointment = Appointment.objects.get(id=appointment_id)
            appointment.check_in_time = datetime.now()
            appointment.is_check_in = True
            appointment.save()
            case = Case.objects.get(appointment=appointment)
            case.status = 1
            case.save()
            return redirect('main.views.receptionist.register_list')    
        else:
            return render_to_response('receptionist/error.htm',{'error':"error"}, context_instance=RequestContext(request))
    else: 
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
    
def schedule_list_view(request):
    if request.user.is_authenticated():
        return render_to_response('receptionist/schedule.htm',{}, context_instance=RequestContext(request))  
    else: 
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    

def timeslot_list(request):
    print "here"
    if request.user.is_authenticated():
        schedule_date = request.POST['rp-schedule-date']
        if len(schedule_date) == 0:
            return render_to_response('receptionist/schedule.htm',{'error':"date cannot be empty"}, context_instance=RequestContext(request))
        format="%m/%d/%Y"
        date = datetime.strptime(schedule_date,format)
        profile = Profile.objects.get(user=request.user)
        schedules = Schedule.objects.filter(mri=profile.mri_id).filter(date=date)
        return render_to_response('receptionist/schedule.htm',{'schedules':schedules}, context_instance=RequestContext(request))
    else: 
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
    
def cancel(request, appointment_id):
    if request.user.is_authenticated():
        if Appointment.objects.filter(id=appointment_id).exists():
            appointment = Appointment.objects.get(id=appointment_id)
            appointment.is_cancelled = True
            appointment.cancelled_by_doctor = False
            appointment.save()
            case = Case.objects.get(appointment=appointment)
            case.status = -1
            case.save()
            return redirect('main.views.receptionist.register_list')    
        else:
            return render_to_response('receptionist/error.htm',{'error':"error"}, context_instance=RequestContext(request))
    else: 
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
def cancel_schedule(request, schedule_id):
    if request.user.is_authenticated():
        if Schedule.objects.filter(id=schedule_id).exists():
            schedule.objects.get(id=schedule_id)
            schedule.delete()
            return redirect('main.views.receptionist.schedule_list_view')    
        else:
            return render_to_response('receptionist/error.htm',{'error':"error"}, context_instance=RequestContext(request))
    else: 
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    

def logs(request):
    if request.user.is_authenticated():
        print "logs"
        profile = Profile.objects.get(user = request.user)
        appointments = Appointment.objects.filter(mri=profile.mri_id).filter(is_check_in = True)
        return render_to_response('receptionist/logs.htm',{'appointments':appointments}, context_instance=RequestContext(request))
    else: 
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
    
    
def register_cancellation_view(request, appointment_id):
    if request.user.is_authenticated():
        if Appointment.objects.filter(id=appointment_id).exists():
            appointment = Appointment.objects.get(id=appointment_id)
            return render_to_response('receptionist/register-cancellation.htm',{'appointment':appointment}, context_instance=RequestContext(request))
    else: 
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
    
def cancel_register(request, appointment_id):
    if request.user.is_authenticated():
        print "hahaha"
        if Appointment.objects.filter(id=appointment_id).exists():
            appointment = Appointment.objects.get(id=appointment_id)
            appointment.is_cancelled = True
            appointment.cancelled_by_doctor = False
            appointment.save()
            case = Case.objects.get(appointment = appointment)
            case.status = -1
            case.save()
            return redirect('main.views.receptionist.logs')    
    else: 
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
    
    
    
