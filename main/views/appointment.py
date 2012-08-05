from django.conf import settings
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
from main.models.message import *

def appointment_view(request, patient_id):
    if request.user.is_authenticated():
        if Patient.objects.filter(id = patient_id).exists():
            patient = Patient.objects.get(id = patient_id)
            return render_to_response('referring/case-create.htm', {'patient':patient},
                                      context_instance=RequestContext(request))
        else:
            return render_to_response('error.htm', {},
                                      context_instance=RequestContext(request))
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
   
def appointment_search(request, patient_id):
    print "aaaaa"
    if request.user.is_authenticated():
        schedule_date = request.POST['preferreddate']
        schedule_time = request.POST['preferredtime']
        zip_code = request.POST['zipcode']
        
        if Patient.objects.filter(id = patient_id).exists():
            patient = Patient.objects.get(id = patient_id)
        else:
            return render_to_response('error.htm', {"error": "No such patient"},
                                      context_instance=RequestContext(request))
    
        errors = []
        if len(zip_code) == 0 and len(schedule_date) == 0 and len(schedule_time) == 0 :
            errors.append("Zip code and date cannot be empty")

        if len(errors) != 0:
            return render_to_response('referring/case-create.htm',{'errors':errors,'patient':patient}, context_instance=RequestContext(request))
        
        dic = {}
        if len(schedule_date) == 0 and len(zip_code) != 0:
            code = int(zip_code)
            upper = code + 500
            lower = code - 500
            centers = MRICenter.objects.exclude(zip__gte=upper).exclude(zip__lte=lower)
            print centers
            for center in centers:
                schedules = Schedule.objects.filter(mri=center).filter(is_available=True).filter(is_cancelled=False)
                print schedules
                if len(schedules) != 0:
                     schedules = Schedule.objects.filter(mri=center).filter(is_available=True).filter(is_cancelled=False).filter(date=schedules[0].date).order_by('start_time')
                     dic[center] = schedules
        elif len(schedule_date) != 0 and len(zip_code) == 0:
            format="%m/%d/%Y"
            date = datetime.strptime(schedule_date,format)
            schedules = Schedule.objects.filter(date = date).filter(is_available = True).filter(is_cancelled = False)
            for schedule in schedules:
                if schedule.mri in dic:
                    timeslot = dic[schedule.mri]
                    timeslot.append(schedule)
                    dic[schedule.mri] = timeslot
                else:
                    timeslot = []
                    timeslot.append(schedule)
                    dic[schedule.mri] = timeslot         
        else:
            format="%m/%d/%Y"
            date = datetime.strptime(schedule_date,format)
            schedules = Schedule.objects.filter(date = date).filter(is_available = True).filter(is_cancelled = False)
            code = int(zipCode)
            upper = code + 500
            lower = code - 500
            centers = []
            for schedule.mri in schedules:
                if schedule.mri.zip <= upper and schedule.mri.zip >= lower:
                    if schedule.mri in dic:
                        timeslot = dic[schedule.mri]
                        timeslot.append(schedule)
                        dic[schedule.mri] = timeslot
                    else:
                        timeslot = []
                        timeslot.append(schedule)
                        dic[schedule.mri] = timeslot
        print dic
        return render_to_response('referring/case-create.htm',{'dic':dic, 'patient':patient}, context_instance=RequestContext(request))  
               
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
    

def make_appointment(request, patient_id, schedule_id):
    print "make - appointment"
    if request.user.is_authenticated():
        error = []
        
    
        if not Patient.objects.filter(id=patient_id).exists():
            error.append("Patient is not exist")
            
        if not Schedule.objects.filter(id=schedule_id).exists():
            error.append("Schedule is not exist")
        
        
        if len(error) != 0:
            return render_to_response('error.htm',{'errors':"No such patient or no such schedule"}, context_instance=RequestContext(request))
        
        patient = Patient.objects.get(id=patient_id)
        schedule = Schedule.objects.get(id=schedule_id)
        doctor = Profile.objects.get(user=request.user)
        mri = schedule.mri
        
        print "here 2"
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
        
        title = patient.first_name + ' ' + patient.last_name + '-APPOINTMENT CONFIRMATION ' + str(schedule.date)
        title = title.upper()
        print title
        content = 'You have already made an appointment: </br>' + 'Patient: ' + patient.first_name + ' ' +  patient.last_name + ' </br> MRI Center: ' + mri.name
       
        content += '</br> Time: ' + str(schedule.date) + '   ' 
   
        content += str(schedule.start_time) + '--' + str(schedule.end_time) + '</br>' 
  
        content += 'Address: ' + mri.address + ' ' + mri.address2 + ',' + mri.city + ',' + mri.state + ',' + str(mri.zip) +'</br>' 

        # content = "You have already made an appointment"
        print content
        message = Message.objects.create(receiver = doctor, case = case, title = title, content = content, type = 0, is_sys = True)
        message.save()
        
        
        return render_to_response('referring/case-create-confirm.htm',{'schedule':schedule, 'appointment':appointment}, context_instance=RequestContext(request))
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    

def appointment_cancel(request, appointment_id):
     if request.user.is_authenticated():
        print "cancel"
        
        errors = []
        
        if not Appointment.objects.filter(id=appointment_id).exists():
            errors.append("No such appointment")
      
        if len(errors) != 0:
            return render_to_response('referring/appointmentConfirm.htm',{'errors':errors}, context_instance=RequestContext(request))
        
        
        appointment = Appointment.objects.get(id=appointment_id)
        schedule = appointment.schedule
        case = appointment.case
        print case
        
        if case.status != 0:
            errors.append("This appointment cannot be cancel")
            return render_to_response('error.htm',{'errors':errors}, context_instance=RequestContext(request))
        else:
            print "here"
            case.status = -1
            case.save()
            schedule.is_available = True
            schedule.save()
            appointment.is_cancelled = True 
            appointment.save()
            patient = appointment.patient
            # create message
            
            patient = appointment.patient
            mri = appointment.mri
            doctor = Profile.objects.get(user = request.user)
            
            # create message
        
            title = patient.first_name + ' ' + patient.last_name + '-APPOINTMENT CONCELLATION ' + str(schedule.date)
            title = title.upper()
            print title
            content = 'You have already CANCELLATION an appointment: </br>' + 'Patient: ' + patient.first_name + ' ' +  patient.last_name + ' </br> MRI Center: ' + mri.name
       
            content += '</br> Time: ' + str(schedule.date) + '   ' 
   
            content += str(schedule.start_time) + '--' + str(schedule.end_time) + '</br>' 
        
            content += 'Address: ' + mri.address + ' ' + mri.address2 + ',' + mri.city + ',' + mri.state + ',' + str(mri.zip) +'</br>' 

            # content = "You have already made an appointment"
            print content
            message = Message.objects.create(receiver = doctor, case = case, title = title, content = content, type = 1, is_sys = True)
            message.save()
           
            print "heihei"
            return redirect('main.views.patients.patientInfo', patient.id, 'False')
     else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    

def appointment_reschedule(request, appointment_id):
    if request.user.is_authenticated():
        if Appointment.objects.filter(id=appointment_id).exists():
            appointment = Appointment.objects.get(id=appointment_id)
            return render_to_response('referring/schedule-change.htm',{'appointment':appointment}, context_instance=RequestContext(request))
        else:
            return render_to_response('referring/schedule-detail.htm',{'errors':"No such schedule"}, context_instance=RequestContext(request))
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))

    
def reappointment_search(request, appointment_id):
    if request.user.is_authenticated():
        schedule_date = request.POST['preferreddate']
        schedule_time = request.POST['preferredtime']
        zip_code = request.POST['zipcode']
        
        if Appointment.objects.filter(id=appointment_id).exists():
            appointment = Appointment.objects.get(id=appointment_id)
            patient = appointment.patient
        else:
            return render_to_response('error.htm',{'errors':"No such schedule"}, context_instance=RequestContext(request))
        
        print "aaaa"
        
        errors = []
        if len(zip_code) == 0 and len(schedule_date) == 0 and len(schedule_time) == 0 :
            errors.append("Zip code and date cannot be empty")

        if len(errors) != 0:
            return render_to_response('referring/schedule-change.htm',{'errors':errors,'patient':patient}, context_instance=RequestContext(request))
        
        dic = {}
        if len(schedule_date) == 0 and len(zip_code) != 0:
            code = int(zip_code)
            upper = code + 500
            lower = code - 500
            centers = MRICenter.objects.exclude(zip__gte=upper).exclude(zip__lte=lower)
            print centers
            for center in centers:
                schedules = Schedule.objects.filter(mri=center).filter(is_available=True).filter(is_cancelled=False)
                print schedules
                if len(schedules) != 0:
                     schedules = Schedule.objects.filter(mri=center).filter(is_available=True).filter(is_cancelled=False).filter(date=schedules[0].date).order_by('start_time')
                     dic[center] = schedules
        elif len(schedule_date) != 0 and len(zip_code) == 0:
            format="%m/%d/%Y"
            date = datetime.strptime(schedule_date,format)
            schedules = Schedule.objects.filter(date = date).filter(is_available = True).filter(is_cancelled = False)
            for schedule in schedules:
                if schedule.mri in dic:
                    timeslot = dic[schedule.mri]
                    timeslot.append(schedule)
                    dic[schedule.mri] = timeslot
                else:
                    timeslot = []
                    timeslot.append(schedule)
                    dic[schedule.mri] = timeslot         
        else:
            format="%m/%d/%Y"
            date = datetime.strptime(schedule_date,format)
            schedules = Schedule.objects.filter(date = date).filter(is_available = True).filter(is_cancelled = False)
            code = int(zipCode)
            upper = code + 500
            lower = code - 500
            centers = []
            for schedule.mri in schedules:
                if schedule.mri.zip <= upper and schedule.mri.zip >= lower:
                    if schedule.mri in dic:
                        timeslot = dic[schedule.mri]
                        timeslot.append(schedule)
                        dic[schedule.mri] = timeslot
                    else:
                        timeslot = []
                        timeslot.append(schedule)
                        dic[schedule.mri] = timeslot
        print dic
        return render_to_response('referring/schedule-change.htm',{'dic':dic, 'patient':patient, 'appointment':appointment}, context_instance=RequestContext(request))  
               
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
    
def remake_appointment(request, patient_id, schedule_id, appointment_id):
    if request.user.is_authenticated():
        error = []
            
        if not Schedule.objects.filter(id=schedule_id).exists():
            error.append("Schedule is not exist")
        
        
        if not Appointment.objects.filter(id=appointment_id).exists():
            error.append("Appointment is not exist")
            
        if len(error) != 0:
            return render_to_response('error.htm',{'errors':"No such patient or no such schedule"}, context_instance=RequestContext(request))
        
        print "here 1"
        old_appointment = Appointment.objects.get(id=appointment_id)
        schedule = Schedule.objects.get(id=schedule_id)
        patient =  old_appointment.patient
        doctor = old_appointment.doctor
        mri = schedule.mri
        case = old_appointment.case
        
        print "here 2"
        # update schedule
        old_appointment.schedule.is_available = True
        old_appointment.is_current = False
        old_appointment.is_cancelled = True
        
        
        schedule.is_available = False
        schedule.save()
        
        # create case
       
       
        
        print "here3"  
        # create appointment
        appointment = Appointment.objects.create(doctor=doctor, patient=patient,schedule=schedule,mri=mri,case=case)
        appointment.save()
        print "here4"
        
        
        # create message
        
        title = patient.first_name + ' ' + patient.last_name + '-Reschedule ' + str(schedule.date)
        title = title.upper()
        print title
        content = 'You have reschedule an appointment: </br>' + 'Patient: ' + patient.first_name + ' ' +  patient.last_name + ' </br> MRI Center: ' + mri.name
       
        content += '</br> Time: ' + str(schedule.date) + '   ' 
   
        content += str(schedule.start_time) + '--' + str(schedule.end_time) + '</br>' 
  
        content += 'Address: ' + mri.address + ' ' + mri.address2 + ',' + mri.city + ',' + mri.state + ',' + str(mri.zip) +'</br>' 

        # content = "You have already made an appointment"
        print content
        message = Message.objects.create(receiver = doctor, case = case, title = title, content = content, type = 2, is_sys = True)
        message.save()
        
        
        return render_to_response('referring/case-create-confirm.htm',{'schedule':schedule, 'appointment':appointment}, context_instance=RequestContext(request))
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
    
     