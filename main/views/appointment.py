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

def appointment_view(request):
    print "appointmentView"
    if request.user.is_authenticated():
        return render_to_response('referring/schedule.htm', {},
                              context_instance=RequestContext(request))
    
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
    
def appointment_search(request):
    print "search"
    if request.user.is_authenticated():
        schedule_date = request.POST['popup-schedule-date']
        zipCode = request.POST['popup-schedule-location']
        
        error = []
        if len(zipCode) == 0:
            error.append("Zip code cannot be empty")
        
                
        if len(error) != 0:
            return render_to_response('referring/schedule.htm',{'error':error}, context_instance=RequestContext(request))
        elif len(schedule_date) == 0:
            code = int(zipCode)
            upper = code + 500
            lower = code - 500
            centers = MRICenter.objects.exclude(zip__gte=upper).exclude(zip__lte=lower)
            print centers
            return render_to_response('referring/schedule.htm',{'centers':centers}, context_instance=RequestContext(request))
        else:
            format="%m/%d/%Y"
            date = datetime.strptime(schedule_date,format)
            schedules = Schedule.objects.filter(date = date).filter(is_available = True)
            code = int(zipCode)
            upper = code + 500
            lower = code - 500
            centers = []
            for schedule in schedules:
                center = schedule.mri 
                if center.zip <= upper and center.zip >= lower:
                    centers.append(center)
                    
            return render_to_response('referring/schedule.htm',{'centers':centers}, context_instance=RequestContext(request))  
               
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
    
def mri_info(request, mri_id):
    print "mri info"
    if request.user.is_authenticated():
        mri = MRICenter.objects.get(id=mri_id)
        
        return render_to_response('referring/mri-info.htm',{'mri':mri}, context_instance=RequestContext(request))
        
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    


def mri_schedule(request, mri_id):
    print "mri schedule"
    if request.user.is_authenticated():
        mri = MRICenter.objects.get(id=mri_id)
        schedules = Schedule.objects.filter(mri=mri).filter(date__gte=datetime.today()).filter(is_available=True).order_by('-date','start_time')
        return render_to_response('referring/center-timeslot.htm',{'schedules':schedules}, context_instance=RequestContext(request))
        
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
    
def schedule_detail(request, schedule_id):
    print "detail"
    if request.user.is_authenticated():
        schedule = Schedule.objects.get(id=schedule_id)
        return render_to_response('referring/schedule-detail.htm',{'schedule':schedule, 'mri':schedule.mri}, context_instance=RequestContext(request))
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))   
    
    
def make_appointment(request, schedule_id):
    print "make - appointment"
    if request.user.is_authenticated():
        error = []
        patient_ssn = request.POST['patient_id']
        patient = Patient.objects.get(ssn=patient_ssn)
        schedule = Schedule.objects.get(id=schedule_id)
        doctor = Profile.objects.get(user=request.user)
        mri = schedule.mri
        
        print patient
        print schedule
        print doctor
        print mri
        if patient is None:
            error.append("Patient ssn is incorrect")
            
        if schedule is None:
            error.append("Schedule id is not exist")
        
        if len(error) != 0:
            return render_to_response('referring/schedule-detail.htm',{'schedule':schedule, 'mri':schedule.mri, 'error':error}, context_instance=RequestContext(request))
        
        print "here"   
        # update schedule
        schedule = Schedule.objects.get(id=schedule_id)
        schedule.is_available = False
        schedule.save()
        
        print "here3"  
        # create appointment
        appointment = Appointment.objects.create(doctor=doctor, patient=patient,schedule=schedule,mri=mri)
        appointment.save()
        print "here4"
        # create case
        case = Case.objects.create(appointment=appointment)
        case.save()
        print "here5"
        return render_to_response('referring/appointmentConfirm.htm',{'schedule':schedule, 'mri':schedule.mri, 'patient':patient}, context_instance=RequestContext(request))
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))   
    

def appointment_cancel(request, appointment_id):
     if request.user.is_authenticated():
        print "cancel"
        appointment = Appointment.objects.get(id=appointment_id)
        schedule = appointment.schedule
        case = Case.objects.get(appointment=appointment)
        error = []
        if case.status != 0:
            error.append("This appointment cannot be cancel")
            return render_to_response('referring/appointmentConfirm.htm',{'error':error}, context_instance=RequestContext(request))
        else:
            case.status = -1
            case.save()
            schedule.is_available = True
            schedule.save()
            appointment.is_cancelled = True 
            appointment.save()
            print "tt"
            return render_to_response('referring/appointmentCancelConfirm.htm',{'schedule':schedule, 'mri':schedule.mri, 'patient':appointment.patient}, context_instance=RequestContext(request))
     else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))   
    
    
     