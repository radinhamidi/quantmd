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
        appointments = Appointment.objects.filter(mri=profile.mri_id).filter(is_check_in = False).filter(is_cancelled = False)
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
            case = appointment.case
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
        schedules = Schedule.objects.filter(mri=profile.mri_id).filter(date=date).filter(is_cancelled=False)
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
            case = appointment.case
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
            schedule.is_cancelled=True
            schedule.save()
            return redirect('main.views.receptionist.schedule_list_view')    
        else:
            return render_to_response('receptionist/error.htm',{'error':"error"}, context_instance=RequestContext(request))
    else: 
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    

def logs(request):
    if request.user.is_authenticated():
        print "logs"
        profile = Profile.objects.get(user = request.user)
        appointments = Appointment.objects.filter(mri=profile.mri_id).filter(is_check_in = True).filter(is_cancelled=False)
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
        if Appointment.objects.filter(id=appointment_id).exists():
            appointment = Appointment.objects.get(id=appointment_id)
            appointment.is_cancelled = True
            appointment.cancelled_by_doctor = False
            appointment.save()
            case = appointment.case
            case.status = -1
            case.save()
            return redirect('main.views.receptionist.logs')    
    else: 
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
    
def reschedule_view(request, appointment_id):
    if request.user.is_authenticated():
        if not Appointment.objects.filter(id = appointment_id).exists():
            return render_to_response('error.htm',{'error': "appointment is not exist"}, context_instance=RequestContext(request))
        print "success0"
        request.session['appointment_id'] = appointment_id
        print "success"
        return render_to_response('receptionist/reschedule.htm',{}, context_instance=RequestContext(request))
    else: 
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
def reschedule_list_view(request):
    if request.user.is_authenticated():
        schedule_date = request.POST['rp-reschedule-date']
        if len(schedule_date) == 0:
            return render_to_response('receptionist/reschedule.htm',{'error':"date cannot be empty"}, context_instance=RequestContext(request))
        format="%m/%d/%Y"
        date = datetime.strptime(schedule_date,format)
        profile = Profile.objects.get(user=request.user)
        schedules = Schedule.objects.filter(mri=profile.mri_id).filter(date=date).filter(is_cancelled=False)
        print schedules
        return render_to_response('receptionist/reschedule.htm',{'schedules':schedules}, context_instance=RequestContext(request))
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
    
def reschedule_action(request, schedule_id):
    if request.user.is_authenticated():
        if not Schedule.objects.filter(id = schedule_id).exists():
            return render_to_response('receptionist/reschedule.htm',{'error':"Schedule is not available"}, context_instance=RequestContext(request))
        
        print "haha"
        appointment_id = request.session['appointment_id']
        if appointment_id is None:
            return render_to_response('receptionist/reschedule.htm',{'error':"Appointment is not available"}, context_instance=RequestContext(request))
        
        print "heihei"
        # old_appointment cancelled
        old_appointment = Appointment.objects.get(id = appointment_id)
        old_appointment.is_cancelled = True
        # old_schedule available
        old_schedule = old_appointment.schedule
        old_schedule.is_available = True
        
        new_schedule = Schedule.objects.get(id = schedule_id)
        new_schedule.is_available = False
        
        new_appointment = Appointment.objects.create(doctor = old_appointment.doctor, patient = old_appointment.patient, schedule = new_schedule, case = old_appointment.case, mri = old_appointment.mri)
        
        old_appointment.save()
        old_schedule.save()
        new_schedule.save()
        new_appointment.save()
        
        print "success"
        return redirect('main.views.receptionist.register_list')    
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))