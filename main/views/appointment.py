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
    if request.user.is_authenticated():
        return render_to_response('referring/schedule.htm', {},
                              context_instance=RequestContext(request))
    
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
    
def appointment_search(request):
    print "search"
    if request.user.is_authenticated():
        schedule_date = request.POST['popup-schedule-date']
        zip_code = request.POST['popup-schedule-location']
        
        errors = []
        if len(zip_code) == 0 and len(schedule_data) == 0:
            errors.append("Zip code and date cannot be empty")
                 
        if len(errors) != 0:
            return render_to_response('referring/schedule.htm',{'errors':errors}, context_instance=RequestContext(request))
        
        if len(schedule_date) == 0 and len(zip_code) != 0:
            code = int(zip_code)
            upper = code + 500
            lower = code - 500
            centers = MRICenter.objects.exclude(zip__gte=upper).exclude(zip__lte=lower)
        elif len(schedule_date) != 0 and len(zip_code) == 0:
            format="%m/%d/%Y"
            date = datetime.strptime(schedule_date,format)
            schedules = Schedule.objects.filter(date = date).filter(is_available = True).filter(is_cancelled = False)
            centers = []
            for schedule in schedules:
                centers.append(schedule.mri)
        else:
            format="%m/%d/%Y"
            date = datetime.strptime(schedule_date,format)
            schedules = Schedule.objects.filter(date = date).filter(is_available = True).filter(is_cancelled = False)
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
    if request.user.is_authenticated():
        
        if not MRICenter.objects.filter(id = mri_id).exists():
            return render_to_response('referring/mri-info.htm',{'error': "MRI center do not exist"}, context_instance=RequestContext(request))
        
        mri = MRICenter.objects.get(id=mri_id)
        
        return render_to_response('referring/mri-info.htm',{'mri':mri}, context_instance=RequestContext(request))
        
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    


def mri_schedule(request, mri_id):
    print "mri schedule"
    if request.user.is_authenticated():
        if MRICenter.objects.filter(id=mri_id).exists():
            mri = MRICenter.objects.get(id=mri_id)
            schedules = Schedule.objects.filter(mri=mri).filter(date__gte=datetime.today()).filter(is_available=True).filter(is_cancelled = False).order_by('-date','start_time')
            return render_to_response('referring/center-timeslot.htm',{'schedules':schedules}, context_instance=RequestContext(request))
        else:
            return render_to_response('referring/center-timeslot.htm',{'errors':"No such MRI center"}, context_instance=RequestContext(request))
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
    
def schedule_detail(request, schedule_id):
    print "detail"
    if request.user.is_authenticated():
        if Schedule.objects.filter(id=schedule_id).exists():
            schedule = Schedule.objects.get(id=schedule_id)
            return render_to_response('referring/schedule-detail.htm',{'schedule':schedule, 'mri':schedule.mri}, context_instance=RequestContext(request))
        else:
            return render_to_response('referring/schedule-detail.htm',{'errors':"No such schedule"}, context_instance=RequestContext(request))
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))   
    

def make_appointment(request, schedule_id):
    print "make - appointment"
    if request.user.is_authenticated():
        error = []
        patient_id = request.POST['patient_id']
        
    
        if Patient.objects.filter(id=patient_id).exists():
            error.append("Patient is not exist")
            
        if Schedule.objects.filter(id=schedule_id).exists():
            error.append("Schedule is not exist")
        
        
        if len(error) != 0:
            return render_to_response('referring/schedule-detail.htm',{'error':error}, context_instance=RequestContext(request))
        
        patient = Patient.objects.get(ssn=patient_id)
        schedule = Schedule.objects.get(id=schedule_id)
        doctor = Profile.objects.get(user=request.user)
        mri = schedule.mri
        
        # update schedule
        schedule = Schedule.objects.get(id=schedule_id)
        schedule.is_available = False
        schedule.save()
        
        
         # create case
        case = Case.objects.create()
        case.save()
        
        print "here3"  
        # create appointment
        appointment = Appointment.objects.create(doctor=doctor, patient=patient,schedule=schedule,mri=mri,case=case)
        appointment.save()
        print "here4"
       
        # create message
        title = patient.first_name + " " + patient.last_name + "-APPOINTMENT CONFIRMATION" + schedule.date
        title = title.upper()
        content = "You have already made an appointment: </br>" + "Patient: " + patient.first_name + " " +  patient.last_name + " </br> MRI Center: " + mri.name +"</br>" + "Time: " + schedule.date + "   " + schedule.start_time + "--" + schedule.end_time + "</br>" + "Address: " + mri.address1 + " " + mri.address2 + "," + mri.city + "," + mri.state + "," + mri.zip +"</br>" 
        message = Message.objects.create(receiver = doctor, case = case, title = title, content = content, type = 0)
        message.save()
        
        print message
        
        return render_to_response('referring/appointmentConfirm.htm',{'schedule':schedule, 'mri':mri, 'patient':patient}, context_instance=RequestContext(request))
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    

def appointment_cancel(request, appointment_id):
     if request.user.is_authenticated():
        print "cancel"
        
        errors = []
        
        if Appointment.objects.filter(id=appointment_id).exist():
            errors.append("No such appointment")
        
        if len(errors) != 0:
            return render_to_response('referring/appointmentConfirm.htm',{'errors':errors}, context_instance=RequestContext(request))
        
        
        appointment = Appointment.objects.get(id=appointment_id)
        schedule = appointment.schedule
        case = appointment.case
        
        if case.status != 0:
            errors.append("This appointment cannot be cancel")
            return render_to_response('referring/appointmentConfirm.htm',{'errors':errors}, context_instance=RequestContext(request))
        else:
            case.status = -1
            case.save()
            schedule.is_available = True
            schedule.save()
            appointment.is_cancelled = True 
            appointment.save()
            
            # create message
            patient = appointment.patient
            mri = appointment.mri
            doctor = Profile.objects.get(user = request.user)
            
            title = patient.first_name + " " + patient.last_name + "-APPOINTMENT  CONCELLATION" + schedule.date
            title = title.upper()
            content = "You have already concelled an appointment: </br>" + "Patient: " + patient.first_name + " " +  patient.last_name + " </br> MRI Center: " + mri.name +"</br>" + "Time: " + schedule.date + "   " + schedule.start_time + "--" + schedule.end_time + "</br>" + "Address: " + mri.address1 + " " + mri.address2 + "," + mri.city + "," + mri.state + "," + mri.zip +"</br>" 
            message = Message.objects.create(receiver = doctor, case = case, title = title, content = content, type = 1)
            message.save()
                
            return render_to_response('referring/appointmentCancelConfirm.htm',{'schedule':schedule, 'mri':schedule.mri, 'patient':appointment.patient}, context_instance=RequestContext(request))
     else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))   
    
    
     