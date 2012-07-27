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
        profile = Profile.objects.get(user = request.user)
        appointments = Appointment.objects.filter(mri=profile.mri_id)
        appointment_set = []
        for appointment in appointments:
            case = Case.objects.get(appointment=appointment)
            if case.status == 0:
                appointment_set.append(appointment)
        print appointment_set
        return render_to_response('receptionist/register.htm',{'appointments':appointment_set}, context_instance=RequestContext(request))  
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
    print "here"
    if request.user.is_authenticated():
        if Schedule.objects.filter(id=schedule_id).exists():
            schedule.objects.get(id=schedule_id)
            schedule.delete()
            print "aaaa"
            return redirect('main.views.receptionist.schedule_list_view')    
        else:
            return render_to_response('receptionist/error.htm',{'error':"error"}, context_instance=RequestContext(request))
    else: 
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
