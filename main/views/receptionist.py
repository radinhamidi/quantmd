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
from main.models.message import *
import datetime
import operator
import time
from MySQLdb.constants.FIELD_TYPE import NULL
from django.template import loader, Context
from django.core.mail import send_mail

@login_required
def register_list(request):
    profile = Profile.objects.get(user = request.user)
    mri = profile.mri_id
    today = datetime.datetime.now().date()
    today_appointments = Appointment.objects.filter(mri=profile.mri_id, is_cancelled = False, is_current = True, schedule__date= today,case__status=0)
    today_checkin_appointments = Appointment.objects.filter(mri=profile.mri_id, is_cancelled = False, is_current = True, schedule__date=today,case__status=1)
    
    return render_to_response('receptionist/today.htm',{'appointments':today_appointments, 'checkins':  today_checkin_appointments, 'mri':mri}, context_instance=RequestContext(request))  


@login_required    
def check_out(request, appointment_id):
    if Appointment.objects.filter(id=appointment_id).exists():
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.check_out_time = datetime.datetime.now()
        appointment.is_check_out = True
        appointment.save()
        return redirect('main.views.receptionist.register_list') 
    else:
        return render_to_response('receptionist/error.htm',{'error':"error"}, context_instance=RequestContext(request))

@login_required
def check_in(request, appointment_id):
    if Appointment.objects.filter(id=appointment_id).exists():
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.check_in_time = datetime.datetime.now()
        appointment.is_check_in = True
        appointment.case_status = 1
        appointment.save()
        case = appointment.case
        case.status = 1
        case.save()
        print "hihihi"
        return redirect('main.views.receptionist.register_list')    
    else:
        return render_to_response('receptionist/error.htm',{'error':"error"}, context_instance=RequestContext(request))

@login_required
def check_in_confirm(request, appointment_id):
    if Appointment.objects.filter(id=appointment_id).exists():
        appointment = Appointment.objects.get(id=appointment_id)
        date = datetime.datetime.now()
        return render_to_response('receptionist/patient-checkin.htm',{'appointment':appointment, 'date':date}, context_instance=RequestContext(request))
    else:
        return render_to_response('receptionist/error.htm',{'error':"error"}, context_instance=RequestContext(request))

@login_required
def check_in_cancell(request, appointment_id):
    if Appointment.objects.filter(id=appointment_id).exists():
        appointment = Appointment.objects.get(id=appointment_id)
        
        if appointment.case.status > 1:
            messages.error(request, 'This case already upload MRI data, it cannot be cancelled')
            return redirect('main.views.receptionist.register_list') 

        appointment.check_in_time = None
        appointment.is_check_in = False
        appointment.case_status = 0
        appointment.save()
        case = appointment.case
        case.status = 0
        case.save()
        date = datetime.datetime.now()
        return render_to_response('receptionist/checkin-cancel-confirm.htm',{'patient':appointment.patient, 'date':date}, context_instance=RequestContext(request))
    else:
        return render_to_response('receptionist/error.htm',{'error':"error"}, context_instance=RequestContext(request))

@login_required
def schedule_list_view(request, month):
    mri = Profile.objects.get(user = request.user).mri_id
    today = datetime.datetime.now()
    month = int(month)
    days = month * 30
    if month != 0:
        if month > 0:
            days = month * 30
            today = today + datetime.timedelta(days = days)
        else:
            days = abs(month) * 30
            today = today - datetime.timedelta(days = days)
    today = today.replace(day=1)    
    date = today
    current = today.month
    dic = {}
    while today.month == current:
        schedules = Schedule.objects.filter(mri = mri, date = today.date(), is_cancelled = False).order_by('start_time')
        dic[today.date()] = schedules
        today = today + datetime.timedelta(days = 1)
    
    sorted_x = sorted(dic.iteritems(), key=operator.itemgetter(0), reverse=False)
    return render_to_response('receptionist/schedule.htm',{'dic':sorted_x, 'date': date, 'month': month}, context_instance=RequestContext(request))  

@login_required
def amend_timesolt(request, month):
    mri = Profile.objects.get(user = request.user).mri_id
    today = datetime.datetime.now()
    month = int(month)
    days = month * 30
    if month != 0:
        if month > 0:
            days = month * 30
            today = today + datetime.timedelta(days = days)
        else:
            days = abs(month) * 30
            today = today - datetime.timedelta(days = days)
    today = today.replace(day=1)    
    date = today
    current = today.month
    dic = {}
    while today.month == current:
        schedules = Schedule.objects.filter(mri = mri, date = today.date(), is_cancelled = False).order_by('start_time')
        dic[today.date()] = schedules
        today = today + datetime.timedelta(days = 1)
    
    sorted_x = sorted(dic.iteritems(), key=operator.itemgetter(0), reverse=False)
    return render_to_response('receptionist/schedule-modify.htm',{'dic':sorted_x, 'date': date, 'month': month}, context_instance=RequestContext(request))  

@login_required
def add_timesolt(request, year, month, day):
    timeslots = request.POST['newtimeslot']
    date = datetime.datetime(int(year),int(month),int(day))
    mri = Profile.objects.get(user = request.user).mri_id
    today = datetime.datetime.now().month
    month = int(month) - today
    errors = []
    if len(timeslots) == 0:
        errors.append("Please enter new timeslots")
    if date.date() < datetime.datetime.now().date():
        errors.append("You do not need to amend the schedule before today")
        
    if len(errors) != 0:
        return redirect('main.views.receptionist.amend_timesolt', month)
        
    times = timeslots.split(';')
  
    for str in times:
        try:
            str_now = time.strptime(str, "%H:%M")
        except ValueError:
            return redirect('main.views.receptionist.amend_timesolt', month)  
            
        
        str_now = datetime.datetime(* str_now[:6]).time()
        
        if not Schedule.objects.filter(date=date).filter(is_cancelled = False).filter(start_time = str_now).exists():
            schedule = Schedule.objects.create(mri = mri, date = date, start_time = str_now, end_time = str_now)
            schedule.save()
    return redirect('main.views.receptionist.amend_timesolt', month)    

@login_required
def patients_view(request):
    profile = Profile.objects.get(user = request.user)
    mri = profile.mri_id
    
    appointments = Appointment.objects.filter(mri = mri, is_current = True, is_cancelled = False, is_check_in = False)
    return render_to_response('receptionist/patients.htm',{'appointments':appointments}, context_instance=RequestContext(request))  

@login_required    
def cancel(request, appointment_id):
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

@login_required    
def cancel_schedule(request, schedule_id, month):
    if Schedule.objects.filter(id=schedule_id).exists():
        schedule = Schedule.objects.get(id=schedule_id)
        schedule.is_cancelled=True
        schedule.save()
        print "success"
        return redirect('main.views.receptionist.amend_timesolt', month)    
    else:
        return render_to_response('receptionist/error.htm',{'error':"error"}, context_instance=RequestContext(request))

@login_required 
def logs(request):
    profile = Profile.objects.get(user = request.user)
    appointments = Appointment.objects.filter(mri=profile.mri_id).filter(is_check_in = True).filter(is_cancelled=False).filter(is_current=True).order_by('-id')
    return render_to_response('receptionist/logs.htm',{'appointments':appointments}, context_instance=RequestContext(request))

    
@login_required     
def register_cancellation_view(request, appointment_id):
    if Appointment.objects.filter(id=appointment_id).exists():
        appointment = Appointment.objects.get(id=appointment_id)
        return render_to_response('receptionist/register-cancellation.htm',{'appointment':appointment}, context_instance=RequestContext(request))

@login_required    
def cancel_register(request, appointment_id):
    if Appointment.objects.filter(id=appointment_id).exists():
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.is_cancelled = True
        appointment.cancelled_by_doctor = False
        appointment.save()
        case = appointment.case
        case.status = -1
        case.save()
        return redirect('main.views.receptionist.logs')    
    
@login_required   
def reschedule_view2(request, appointment_id):
    if not Appointment.objects.filter(id = appointment_id).exists():
        return render_to_response('error.htm',{'error': "appointment is not exist"}, context_instance=RequestContext(request))
    appointment = Appointment.objects.get(id = appointment_id)
    print "aaaa"
    return render_to_response('receptionist/patient-reschedule-2.htm',{'appointment':appointment}, context_instance=RequestContext(request))

@login_required 
def reschedule_list_view2(request, appointment_id):
    schedule_date = request.POST['rebookingdate']
    appointment = Appointment.objects.get(id = appointment_id)
    
    errors = []
    if len(schedule_date) == 0:
        errors.append('Date cannot be empty')
    else:   
        try:
            format="%m/%d/%Y"
            date = datetime.datetime.strptime(schedule_date,format)
            
            if date.date() < datetime.datetime.now().date():
                errors.append('Please choose another day, you cannot make an new appointment before today')
        except ValueError:
            errors.append('Incorrect date format')
                     
    if len(errors) != 0:
        return render_to_response('receptionist/patient-reschedule-2.htm',{'errors':errors, 'appointment':appointment}, context_instance=RequestContext(request))
    
    mri = appointment.mri
    
    format="%m/%d/%Y"
    date = datetime.datetime.strptime(schedule_date,format)
    
    count = 0;
    dic = {}
    while count < 10:
        schedules = Schedule.objects.filter(mri = mri, date = date.date(), is_available = True, is_cancelled = False)
        dic[date.date()] = schedules
        date = date + datetime.timedelta(days = 1)
        count += 1
    sorted_x = sorted(dic.iteritems(), key=operator.itemgetter(0), reverse=False)
    
    return render_to_response('receptionist/patient-reschedule-2.htm',{'dic':sorted_x, 'appointment':appointment}, context_instance=RequestContext(request))

@login_required 
def reschedule_action2(request, schedule_id, appointment_id):
    errors = []
    if not Schedule.objects.filter(id = schedule_id).exists():
        errors.append('Schedule is not available')
        
    new_schedule = Schedule.objects.get(id = schedule_id)
    
    if new_schedule.date < datetime.datetime.now().date() or (new_schedule.date == datetime.datetime.now().date() and new_schedule.start_time < datetime.datetime.now().time()):
        errors.append('Please choose another day, you cannot make an appointment before today')
    
    if len(errors) != 0: 
        return render_to_response('receptionist/patient-reschedule-2.htm',{'errors':errors}, context_instance=RequestContext(request))
    
    
    # old_appointment cancelled
    old_appointment = Appointment.objects.get(id = appointment_id)
    old_appointment.is_cancelled = True
    old_appointment.is_current = False
    # old_schedule available
    old_schedule = old_appointment.schedule
    old_schedule.is_available = True
    
    new_schedule.is_available = False
    
    new_appointment = Appointment.objects.create(doctor = old_appointment.doctor, patient = old_appointment.patient, schedule = new_schedule, case = old_appointment.case, mri = old_appointment.mri)
    
    doctor = old_appointment.doctor
    mri = old_appointment.mri
      # create message
    
    title = 'Reschedule for CASE #' + str(old_appointment.case.id) 
    title = title.upper()
    
    content = 'MRI center have reschedule an appointment for your patient: '
    
    content += 'Patient: ' + old_appointment.patient.first_name + ' ' +  old_appointment.patient.last_name 
    
    content = 'You orginal appointment is: ' + 'at ' + old_appointment.mri.name +' on ' + str(old_appointment.schedule.date) + ' at ' + str(old_appointment.schedule.start_time)
    
    content += 'New appointment is:  at ' + mri.name
    
    content += ' on ' + str(new_schedule.date) + '   ' 
    
    content += str(new_schedule.start_time)
    
    content += ' Address is: ' + mri.address + ' ' + mri.address2 + ',' + mri.city + ',' + mri.state + ',' + str(mri.zip)
    
    # content = "You have already made an appointment"
    print content
    message = Message.objects.create(receiver = doctor, case = old_appointment.case, title = title, content = content, type = 2, is_sys = True)
    message.save()
    
    
    old_appointment.save()
    old_schedule.save()
    new_schedule.save()
    new_appointment.save()
    
    '''
    send message
    '''
    services = old_appointment.case.services.all()
    service = ''
    
    for s in services:
        service += s.name + ' '
    
    t = loader.get_template('receptionist/remake_appointment.txt')
    c = Context({
                 'patient': old_appointment.patient,
                 'mri': mri,
                 'schedule':new_schedule,
                 'services':service,
                 'old_schedule': old_appointment.schedule,
                 })
    send_mail('Your appointment have been rescheduled at QuantMD', t.render(c), 'service@quant.md', (old_appointment.patient.email,), fail_silently=False)
    
    return redirect('main.views.receptionist.patients_view')    

    
@login_required     
def reschedule_view(request, appointment_id):
    if not Appointment.objects.filter(id = appointment_id).exists():
        return render_to_response('error.htm',{'error': "appointment is not exist"}, context_instance=RequestContext(request))
    appointment = Appointment.objects.get(id = appointment_id)
    print "aaaa"
    return render_to_response('receptionist/patient-reschedule.htm',{'appointment':appointment}, context_instance=RequestContext(request))

@login_required 
def reschedule_list_view(request, appointment_id):
    schedule_date = request.POST['rebookingdate']
    appointment = Appointment.objects.get(id = appointment_id)
    print schedule_date
    errors = []
    
    if len(schedule_date) == 0:
        errors.append('Date cannot be empty')
    else:   
        try:
            format="%m/%d/%Y"
            date = datetime.datetime.strptime(schedule_date,format)
            
            if date.date() < datetime.datetime.now().date():
                errors.append('Please choose another day, you cannot make an new appointment before today')
        except ValueError:
            errors.append('Incorrect date format')
                     
    if len(errors) != 0:
        return render_to_response('receptionist/patient-reschedule.htm',{'errors':errors, 'appointment':appointment}, context_instance=RequestContext(request))
    
    mri = appointment.mri
    
    format="%m/%d/%Y"
    date = datetime.datetime.strptime(schedule_date,format)
    print date
    count = 0;
    dic = {}
    while count < 10:
        schedules = Schedule.objects.filter(mri = mri, date = date.date(), is_available = True, is_cancelled = False)
        dic[date.date()] = schedules
        date = date + datetime.timedelta(days = 1)
        count += 1
    sorted_x = sorted(dic.iteritems(), key=operator.itemgetter(0), reverse=False)
    print sorted_x
    print "success"
    return render_to_response('receptionist/patient-reschedule.htm',{'dic':sorted_x, 'appointment':appointment}, context_instance=RequestContext(request))

@login_required
def reschedule_action(request, schedule_id, appointment_id):
    errors = []
    if not Schedule.objects.filter(id = schedule_id).exists():
        errors.append('Schedule is not available')
    
    new_schedule = Schedule.objects.get(id = schedule_id)
       
    if new_schedule.date < datetime.datetime.now().date() or (new_schedule.date == datetime.datetime.now().date() and new_schedule.start_time < datetime.datetime.now().time()):
        errors.append('Please choose another day, you cannot make an appointment before today')
    
    print "ccc"
    if len(errors) != 0:
        return render_to_response('receptionist/patient-reschedule.htm',{'errors':errors}, context_instance=RequestContext(request))
    
    # old_appointment cancelled
    
    old_appointment = Appointment.objects.get(id = appointment_id)
    print old_appointment
    old_appointment.is_cancelled = True
    old_appointment.is_current = False
    
    # old_schedule available
    old_schedule = old_appointment.schedule
    old_schedule.is_available = True
    print "hahahahah"
    
    new_schedule.is_available = False
    
    new_appointment = Appointment.objects.create(doctor = old_appointment.doctor, patient = old_appointment.patient, schedule = new_schedule, case = old_appointment.case, mri = old_appointment.mri)
    
    mri = old_appointment.mri
    doctor = old_appointment.doctor
    # create message
    
    title = 'Reschedule for CASE #' + str(old_appointment.case.id) 
    title = title.upper()
    print title
    content = 'MRI center have reschedule an appointment for your patient: '
    print content
    content += 'Patient: ' + old_appointment.patient.first_name + " " + old_appointment.patient.last_name
    print content
    content = 'The orginal appointment is: ' + 'MRI Center: ' + old_appointment.mri.name +' Time: ' + str(old_appointment.schedule.date) + ' at ' + str(old_appointment.schedule.start_time)
    print content
    content += 'New appointment is:   MRI Center: ' + mri.name
    print content
    content += ' Time: ' + str(new_schedule.date) + ' at ' +  str(new_schedule.start_time)
   

    # content = "You have already made an appointment"
    message = Message.objects.create(receiver = doctor, case = old_appointment.case, title = title, content = content, type = 2, is_sys = True)
    message.save()
   
    old_appointment.save()
    old_schedule.save()
    new_schedule.save()
    new_appointment.save()
    
    '''
    send message
    '''
    services = old_appointment.case.services.all()
    service = ''
    
    for s in services:
        service += s.name + ' '

    t = loader.get_template('receptionist/remake_appointment.txt')
    c = Context({
                 'patient': old_appointment.patient,
                 'mri': mri,
                 'schedule':new_schedule,
                 'services':service,
                 'old_schedule': old_appointment.schedule,
                 })
    send_mail('Your appointment have been rescheduled at QuantMD', t.render(c), 'service@quant.md', (old_appointment.patient.email,), fail_silently=False)
    
    
   
    return redirect('main.views.receptionist.register_list')  
