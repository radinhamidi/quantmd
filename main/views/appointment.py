from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import *
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from main.models.mri import *
from main.models.appointment import *
from django.utils.datetime_safe import datetime

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
            return render_to_response('referring/schedule.htm',{'Error':error}, context_instance=RequestContext(request))
        elif len(schedule_date) == 0:
            code = int(zipCode)
            upper = code + 500
            lower = code - 500
            centers = MRICenter.objects.exclude(zip__gte=upper).exclude(zip__lte=lower)
            print centers
            return render_to_response('referring/schedule.htm',{'Centers':centers}, context_instance=RequestContext(request))
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
                    
            return render_to_response('referring/schedule.htm',{'Centers':centers}, context_instance=RequestContext(request))  
               
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
    
def mri_info(request, mri_id):
    print "mri info"
    if request.user.is_authenticated():
        mri = MRICenter.objects.get(id=mri_id)
        
        return render_to_response('referring/mri-info.htm',{'MRI':mri}, context_instance=RequestContext(request))
        
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    


def mri_schedule(request, mri_id):
    print "mri schedule"
    if request.user.is_authenticated():
        mri = MRICenter.objects.get(id=mri_id)
        schedules = Schedule.objects.filter(mri=mri).filter(date__gte=datetime.today())
        print schedules
        return render_to_response('referring/center-timeslot.htm',{'Schedules':schedules}, context_instance=RequestContext(request))
        
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
    
def schedule_detail(request, schedule_id):
    print "detail"
    if request.user.is_authenticated():
        schedule = Schedule.objects.get(id=schedule_id)
        return render_to_response('referring/schedule-detail.htm',{'Schedule':schedule, 'MRI':schedule.mri}, context_instance=RequestContext(request))
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))   
    
    
def make_appointment(request, schedule_id):
    print "make - appointment"
    if request.user.is_authenticated():
        error = []
        patient_ssn = request.POST['schedule-detail-patientid']
        patient = Patient.objects.get(ssn=patient_id)
        schedule = Schedule.objects.get(id=schedule_id)
        doctor = request.user
        mri = schedule.mri
        if patient is None:
            error.append("Patient id is incorrect")
            
        if schedule is None:
            error.append("Schedule id is not exist")
        
        if len(error) == 0:
            return render_to_response('referring/schedule-detail.htm',{'Schedule':schedule, 'MRI':schedule.mri, 'Error':error}, context_instance=RequestContext(request))
            
        # update schedule
        schedule = Schedule.objects.get(id=schedule_id)
        schedule.is_available = True
        schedule.save()
        
        # create appointment
        appointment = Appointment.create(doctor=doctor, patient=patient,schedule=schedule,mri=mri,is_cancelled=False)
        appointment.save()
        
        # create case
        case = Case.create(appointment=appointment)
        case.save()
        
        return render_to_response('referring/appointmentConfirm.htm',{'Schedule':schedule, 'MRI':schedule.mri, 'Patient':patient}, context_instance=RequestContext(request))
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))   
    
    