from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import *
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from main.models.mri import *
from main.models.appointment import *
from main.models.patient import *
from main.models.account import *
from main.utils.form_check import *
from main.models.case import *
from main.models.message import *
from django.template import loader, Context
from django.core.mail import send_mail
import operator
import datetime

def appointment_view(request, patient_id):
    if request.user.is_authenticated():
        if Patient.objects.filter(id = patient_id).exists():
            patient = Patient.objects.get(id = patient_id)
            appointments = Appointment.objects.filter(patient = patient)
            signal = 1
            for appointment in appointments:
                case = appointment.case
                if case.status >= 0 and case.status < 5:
                    signal = 0
                    break
            
            if signal == 0:
                errors = []
                errors.append('You already have an appointment, you cannot make a new one!')
                patient = Patient.objects.get(id = patient_id)
                appointments = Appointment.objects.filter(patient=patient).order_by('-case')
                sort_appointments = []
                for appointment in appointments:
                    if appointment.is_current:
                        sort_appointments.append(appointment)
                
                return render_to_response('referring/patient-info.htm',{'patient': patient, 'appointments':sort_appointments, 'errors':errors}, context_instance=RequestContext(request)) 
               
                
            return render_to_response('referring/case-create.htm', {'patient':patient},
                                      context_instance=RequestContext(request))
        else:
            return render_to_response('error.htm', {},
                                      context_instance=RequestContext(request))
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
   
def appointment_search(request, patient_id):
    if request.user.is_authenticated():
        schedule_date = request.POST['preferreddate']
        zip_code = request.POST['zipcode']
        
        if Patient.objects.filter(id = patient_id).exists():
            patient = Patient.objects.get(id = patient_id)
        else:
            return render_to_response('error.htm', {"error": "No such patient"},
                                      context_instance=RequestContext(request))
        
        errors = []
        if len(zip_code) == 0 and len(schedule_date) == 0:
            errors.append("Zip code or date cannot be empty")
        if zip_code.strip():
            try:
                zip_code = int(zip_code)    
            except:
                errors.append(request, 'zipcode must be numbers')
        
        if len(schedule_date) != 0 and not IsValidDate(schedule_date):
            errors.append('Please enter correct date format and choose a date before today')
            
        if len(errors) != 0:
            return render_to_response('referring/case-create.htm',{'patient': patient, 'errors':errors}, context_instance=RequestContext(request)) 
        
        dic = {}
        if len(schedule_date) == 0 and len(zip_code) != 0:
            code = int(zip_code)
            upper = code + 500
            lower = code - 500
            centers = MRICenter.objects.exclude(zip__gte=upper).exclude(zip__lte=lower)
            today = datetime.datetime.now().date()
            for center in centers:
                schedules = Schedule.objects.filter(mri=center).filter(is_available=True).filter(is_cancelled=False).filter(date__gte = today)
                print schedules
                if len(schedules) != 0:
                     schedules = Schedule.objects.filter(mri=center).filter(is_available=True).filter(is_cancelled=False).filter(date=schedules[0].date).order_by('start_time')
                     dic[center] = schedules
        elif len(schedule_date) != 0 and len(zip_code) == 0:
            format="%m/%d/%Y"
            date = datetime.datetime.strptime(schedule_date,format)
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
            date = datetime.datetime.strptime(schedule_date,format)
            schedules = Schedule.objects.filter(date = date).filter(is_available = True).filter(is_cancelled = False)
            code = int(zip_code)
            upper = code + 500
            lower = code - 500
            centers = []
            for schedule in schedules:
                if schedule.mri.zip <= upper and schedule.mri.zip >= lower:
                    if schedule.mri in dic:
                        timeslot = dic[schedule.mri]
                        timeslot.append(schedule)
                        dic[schedule.mri] = timeslot
                    else:
                        timeslot = []
                        timeslot.append(schedule)
                        dic[schedule.mri] = timeslot
        if len(dic) == 0 :
            errors.append('No schedule available on that date, please change a date!')
            return render_to_response('referring/case-create.htm',{'errors':errors, 'patient':patient}, context_instance=RequestContext(request))
        
        return render_to_response('referring/case-create.htm',{'dic':dic, 'patient':patient}, context_instance=RequestContext(request))  
               
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
    
def mri_info(request, mri_id):
    if request.user.is_authenticated():
        mri = MRICenter.objects.get(id = mri_id)
        today = datetime.datetime.now()
        current = today.day
        i = 0
        dic = {}
        while i < 7:
            schedules = Schedule.objects.filter(mri = mri, date = today.date(), is_cancelled = False).order_by('start_time')
            dic[today.date()] = schedules
            today = today + datetime.timedelta(days = 1)
            i += 1
        
        sorted_x = sorted(dic.iteritems(), key=operator.itemgetter(0), reverse=False)
        return render_to_response('referring/view-mri-details.htm',{'dic':sorted_x}, context_instance=RequestContext(request))   
        
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
def service_view(request,patient_id, schedule_id):
    if request.user.is_authenticated():
        patient = Patient.objects.get(id = patient_id)
        schedule = Schedule.objects.get(id = schedule_id)
        print patient
        print schedule
        services = Service.objects.filter(is_active = True)
        print services
        return render_to_response('referring/case-create-scans.htm',{'patient':patient, 'schedule':schedule, 'services':services}, context_instance=RequestContext(request))
        
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    

def make_appointment(request):
    print "hahahahaha"
    if request.user.is_authenticated():
        error = []
        patient_id = request.POST['patientId']
        schedule_id = request.POST['scheduleId']
        services = request.POST.getlist('services')
        patient = Patient.objects.get(id=patient_id)
        
        if not Patient.objects.filter(id=patient_id).exists():
            error.append("Patient is not exist")
            
        if not Schedule.objects.filter(id=schedule_id).exists():
            error.append("Schedule is not exist")
        
        schedule = Schedule.objects.get(id=schedule_id)
        if schedule.date < datetime.datetime.now().date() or (schedule.date == datetime.datetime.now().date() and schedule.start_time < datetime.datetime.now().time()):
            error.append('Please choose another day, you cannot make an appointment before today')
            
        if len(error) != 0:
            return render_to_response('referring/case-create.htm',{'errors':error, 'patient':patient}, context_instance=RequestContext(request))
        
        
        doctor = Profile.objects.get(user=request.user)
        mri = schedule.mri
        
        print "here 2"
        # update schedule
        schedule = Schedule.objects.get(id=schedule_id)
        schedule.is_available = False
        schedule.save()
        
        print "here4" 
        # create case
        case = Case.objects.create(patient = patient)
        print "here5"
        case.save()
        
        service_name = []
        for service_id in services:
            service = Service.objects.get(id = service_id)
            service_name.append(service.name)
            service_and_case = ServiceAndCase.objects.create(service = service, case = case)
            service_and_case.save()
        
            
        
        print "here3"
        # create appointment
        appointment = Appointment.objects.create(doctor=doctor, patient=patient,schedule=schedule,mri=mri,case=case)
        appointment.save()
        
        
        # create message
        
        title =  'APPOINTMENT CONFIRMATION for CASE #' +  str(case.id)
        title = title.upper()
        print title
        content ='Patient: ' + patient.first_name + ' ' +  patient.last_name + ' have made an appointment: MRI Center: ' + mri.name
       
        content += 'Time: ' + str(schedule.date) + '   ' 
   
        content += str(schedule.start_time) 
  
        content += ' Address: ' + mri.address + ' ' + mri.address2 + ',' + mri.city + ',' + mri.state + ',' + str(mri.zip) 

        # content = "You have already made an appointment"
        print content
        message = Message.objects.create(receiver = doctor, case = case, title = title, content = content, type = 0, is_sys = True)
        message.save()
        
        '''
        send message
        '''
        service = ''
        
        for name in service_name:
            service += name + ' '

        t = loader.get_template('referring/make_appointment.txt')
        c = Context({
                     'patient': patient,
                     'doctor': doctor,
                     'mri': mri,
                     'schedule':schedule,
                     'services':service,
                     })
        send_mail('Your appointment at QuantMD', t.render(c), 'support@xifenfen.com', (patient.email,), fail_silently=False)
        
        return render_to_response('referring/case-create-confirm.htm',{'schedule':schedule, 'appointment':appointment, 'services': case.services.all()}, context_instance=RequestContext(request))
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
        
            title = 'APPOINTMENT CONCELLATION for CASE #' + str(case.id)
            title = title.upper()
            content = 'Patient: ' + patient.first_name + ' ' +  patient.last_name + ' have cancelled an appointment: MRI Center: ' + mri.name
       
            content += 'Time: ' + str(schedule.date) + '   '
   
            content += str(schedule.start_time) 
        
            content += 'Address: ' + mri.address + ' ' + mri.address2 + ',' + mri.city + ',' + mri.state + ',' + str(mri.zip)

            # content = "You have already made an appointment"
            print content
            message = Message.objects.create(receiver = doctor, case = case, title = title, content = content, type = 1, is_sys = True)
            message.save()
            print "success"
            return redirect('main.views.patients.patientInfo', patient.id)
     else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    

def appointment_reschedule(request, appointment_id):
    if request.user.is_authenticated():
        if Appointment.objects.filter(id=appointment_id).exists():
            appointment = Appointment.objects.get(id=appointment_id)
            return render_to_response('referring/schedule-change.htm',{'appointment':appointment, 'patient':appointment.patient}, context_instance=RequestContext(request))
        else:
            return render_to_response('referring/error.htm',{'error':"No such schedule"}, context_instance=RequestContext(request))
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))

    
def reappointment_search(request, appointment_id):
    if request.user.is_authenticated():
        schedule_date = request.POST['preferreddate']
        zip_code = request.POST['zipcode']
        
        if Appointment.objects.filter(id=appointment_id).exists():
            appointment = Appointment.objects.get(id=appointment_id)
            patient = appointment.patient
        else:
            return render_to_response('referring/error.htm',{'errors':"No such schedule"}, context_instance=RequestContext(request))
        
        errors = []
        if len(zip_code) == 0 and len(schedule_date) == 0:
            errors.append("Zip code and date cannot be empty")
        if zip_code.strip():
            try:
                zip_code = int(zip_code)    
            except:
                errors.append(request, 'zipcode must be numbers')
        
        if len(schedule_date) != 0 and not IsValidDate(schedule_date):
            errors.append('Please enter correct date format and choose a date before today')
            

        if len(errors) != 0:
            return render_to_response('referring/schedule-change.htm',{'errors':errors,'patient':patient,'appointment':appointment}, context_instance=RequestContext(request))
        
        dic = {}
        if len(schedule_date) == 0 and len(zip_code) != 0:
            code = int(zip_code)
            upper = code + 500
            lower = code - 500
            centers = MRICenter.objects.exclude(zip__gte=upper).exclude(zip__lte=lower)
            today = datetime.datetime.now().date()
            for center in centers:
                schedules = Schedule.objects.filter(mri=center).filter(is_available=True).filter(is_cancelled=False).filter(date__gte = today)
                print schedules
                if len(schedules) != 0:
                     schedules = Schedule.objects.filter(mri=center).filter(is_available=True).filter(is_cancelled=False).filter(date=schedules[0].date).order_by('start_time')
                     dic[center] = schedules
        elif len(schedule_date) != 0 and len(zip_code) == 0:
            format="%m/%d/%Y"
            date = datetime.datetime.strptime(schedule_date,format)
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
            date = datetime.datetime.strptime(schedule_date,format)
            schedules = Schedule.objects.filter(date = date).filter(is_available = True).filter(is_cancelled = False)
            code = int(zip_code)
            upper = code + 500
            lower = code - 500
            centers = []
            for schedule in schedules:
                if schedule.mri.zip <= upper and schedule.mri.zip >= lower:
                    if schedule.mri in dic:
                        timeslot = dic[schedule.mri]
                        timeslot.append(schedule)
                        dic[schedule.mri] = timeslot
                    else:
                        timeslot = []
                        timeslot.append(schedule)
                        dic[schedule.mri] = timeslot
                        
        if len(dic) == 0 :
            errors.append('No schedule available on that date, please change a date!')
            return render_to_response('referring/schedule-change.htm',{'errors':errors, 'patient':patient,'appointment':appointment}, context_instance=RequestContext(request))
        return render_to_response('referring/schedule-change.htm',{'dic':dic, 'patient':patient, 'appointment':appointment}, context_instance=RequestContext(request))  
               
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
    
def remake_appointment(request, patient_id, schedule_id, appointment_id):
    print "here"
    if request.user.is_authenticated():
        errors = []
            
        if not Schedule.objects.filter(id=schedule_id).exists():
            errors.append("Schedule is not exist")
        
        
        if not Appointment.objects.filter(id=appointment_id).exists():
            errors.append("Appointment is not exist")
        
        schedule = Schedule.objects.get(id=schedule_id)
        
        
        if schedule.date < datetime.datetime.now().date() or (schedule.date == datetime.datetime.now().date() and schedule.start_time < datetime.datetime.now().time()):
            errors.append('Please choose another day, you cannot make an appointment before today')
        
        if len(errors) != 0:
            appointment = Appointment.objects.get(id=appointment_id)
            return render_to_response('referring/schedule-change.htm',{'appointment':appointment, 'patient':appointment.patient, 'errors':errors}, context_instance=RequestContext(request))
        
        
        old_appointment = Appointment.objects.get(id=appointment_id)
       
        patient =  old_appointment.patient
        doctor = old_appointment.doctor
        mri = schedule.mri
        case = old_appointment.case
        
        
        # update schedule
        old_appointment.schedule.is_available = True
        old_appointment.is_current = False
        old_appointment.is_cancelled = True
        
        old_appointment.schedule.save()
        old_appointment.save()
        
        schedule.is_available = False
        schedule.save()
        # create case
        
       
        # create appointment
        appointment = Appointment.objects.create(doctor=doctor, patient=patient,schedule=schedule,mri=mri,case=case)
        appointment.save()
        
        # create message
        
        title = 'Reschedule for CASE #' + str(case.id) 
        title = title.upper()
        print title
        content = 'Patient: ' + patient.first_name + ' ' +  patient.last_name + ' have reschedule an appointment:'
        print content
        content += 'The original appointment is: ' + 'MRI Center: ' + old_appointment.mri.name +'  Time: ' + str(old_appointment.schedule.date) + ' at ' + str(old_appointment.schedule.start_time)
        
        content += 'New appointment is:  MRI Center: ' + mri.name
       
        content += ' Time: ' + str(schedule.date) + ' ' 
        
        content += str(schedule.start_time)
  
        content += 'Address: ' + mri.address + ' ' + mri.address2 + ',' + mri.city + ',' + mri.state + ',' + str(mri.zip) 
        
        # content = "You have already made an appointment"
        print content
        message = Message.objects.create(receiver = doctor, case = case, title = title, content = content, type = 2, is_sys = True)
        message.save()
        
        '''
        send message
        '''
        services = case.services.all()
        service = ''
        
        for s in services:
            service += s.name + ' '

        t = loader.get_template('referring/remake_appointment.txt')
        c = Context({
                     'patient': patient,
                     'doctor': doctor,
                     'mri': mri,
                     'schedule':schedule,
                     'services':service,
                     'old_schedule': old_appointment.schedule,
                     'old_mri': old_appointment.mri,
                     })
        send_mail('Your appointment have been rescheduled at QuantMD', t.render(c), 'support@xifenfen.com', (patient.email,), fail_silently=False)
        
        
        
        
    
        return render_to_response('referring/case-create-confirm.htm',{'schedule':schedule, 'appointment':appointment}, context_instance=RequestContext(request))
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
    
     