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
import datetime
import operator
import time
from MySQLdb.constants.FIELD_TYPE import NULL


def register_list(request):
    print "heihei"
    if request.user.is_authenticated():
        profile = Profile.objects.get(user = request.user)
        mri = profile.mri_id
        appointments = Appointment.objects.filter(mri=profile.mri_id).filter(is_cancelled = False)
        today_appointments = []
        today_checkin_appointments = []
        for appointment in appointments:
            schedule = appointment.schedule
            if schedule.date == datetime.datetime.now().date():
                if appointment.is_check_in:
                    today_checkin_appointments.append(appointment)
                else:
                    today_appointments.append(appointment)
        print "finish"
        return render_to_response('receptionist/today.htm',{'appointments':today_appointments, 'checkins':  today_checkin_appointments, 'mri':mri}, context_instance=RequestContext(request))  
    else: 
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
def check_out(request, appointment_id):
    if request.user.is_authenticated():
        if Appointment.objects.filter(id=appointment_id).exists():
            appointment = Appointment.objects.get(id=appointment_id)
            appointment.check_out_time = datetime.datetime.now()
            appointment.is_check_out = True
            appointment.save()
            return redirect('main.views.receptionist.register_list') 
        else:
            return render_to_response('receptionist/error.htm',{'error':"error"}, context_instance=RequestContext(request))
    else: 
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
def check_in(request, appointment_id):
    print "here"
    if request.user.is_authenticated():
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
    else: 
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
def check_in_confirm(request, appointment_id):
    if request.user.is_authenticated():
        if Appointment.objects.filter(id=appointment_id).exists():
            appointment = Appointment.objects.get(id=appointment_id)
            date = datetime.datetime.now()
            return render_to_response('receptionist/patient-checkin.htm',{'appointment':appointment, 'date':date}, context_instance=RequestContext(request))
        else:
            return render_to_response('receptionist/error.htm',{'error':"error"}, context_instance=RequestContext(request))
    else: 
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
def check_in_cancell(request, appointment_id):
    print "here"
    if request.user.is_authenticated():
        if Appointment.objects.filter(id=appointment_id).exists():
            appointment = Appointment.objects.get(id=appointment_id)
            print appointment
            appointment.check_in_time = None
            appointment.is_check_in = False
            appointment.case_status = 0
            appointment.save()
            case = appointment.case
            case.status = 0
            case.save()
            print "hihihi"
            return redirect('main.views.receptionist.register_list')    
        else:
            return render_to_response('receptionist/error.htm',{'error':"error"}, context_instance=RequestContext(request))
    else: 
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    

def schedule_list_view(request, month):
    print "hehe"
    if request.user.is_authenticated():
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
            schedules = Schedule.objects.filter(mri = mri, date = today.date(), is_cancelled = False)
            dic[today.date()] = schedules
            today = today + datetime.timedelta(days = 1)
        
        sorted_x = sorted(dic.iteritems(), key=operator.itemgetter(0), reverse=False)
        print sorted_x
        return render_to_response('receptionist/schedule.htm',{'dic':sorted_x, 'date': date, 'month': month}, context_instance=RequestContext(request))  
    else: 
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))

def amend_timesolt(request, month):
    if request.user.is_authenticated():
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
            schedules = Schedule.objects.filter(mri = mri, date = today.date(), is_cancelled = False)
            dic[today.date()] = schedules
            today = today + datetime.timedelta(days = 1)
        
        sorted_x = sorted(dic.iteritems(), key=operator.itemgetter(0), reverse=False)
        print sorted_x
        return render_to_response('receptionist/schedule-modify.htm',{'dic':sorted_x, 'date': date, 'month': month}, context_instance=RequestContext(request))  
    else: 
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
def add_timesolt(request, year, month, day):
    if request.user.is_authenticated():
        timeslots = request.POST['newtimeslot']
        date = datetime.datetime(int(year),int(month),int(day))
        mri = Profile.objects.get(user = request.user).mri_id
        
        error = []
        if len(timeslots) == 0:
            error.append("Please enter new timeslots")
        
        print "zheli"
        print timeslots
        times = timeslots.split(';')
        print times
        print "zheli2"
        for str in times:
            str_now = time.strptime(str, "%H:%M")
            str_now = datetime.datetime(* str_now[:6]).time()
            print str_now
            if not Schedule.objects.filter(is_cancelled = False).filter(start_time = str_now).exists():
                "zheli3"
                schedule = Schedule.objects.create(mri = mri, date = date, start_time = str_now, end_time = str_now)
                schedule.save()
                print "heihei"
        print "success"
        today = datetime.datetime.now().month
        month = int(month) - today
        print month
        return redirect('main.views.receptionist.amend_timesolt', month)    
    else: 
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))

def patients_view(request):
    if request.user.is_authenticated():
        profile = Profile.objects.get(user = request.user)
        mri = profile.mri_id
        
        appointments = Appointment.objects.filter(mri = mri, is_current = True, is_cancelled = False, is_check_in = False)
        return render_to_response('receptionist/patients.htm',{'appointments':appointments}, context_instance=RequestContext(request))  
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
        profile = Profile.objects.get(user = request.user)
        appointments = Appointment.objects.filter(mri=profile.mri_id).filter(is_check_in = True).filter(is_cancelled=False).filter(is_current=True).order_by('-id')
        print appointments
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
    
    
def reschedule_view2(request, appointment_id):
    if request.user.is_authenticated():
        if not Appointment.objects.filter(id = appointment_id).exists():
            return render_to_response('error.htm',{'error': "appointment is not exist"}, context_instance=RequestContext(request))
        appointment = Appointment.objects.get(id = appointment_id)
        print "aaaa"
        return render_to_response('receptionist/patient-reschedule-2.htm',{'appointment':appointment}, context_instance=RequestContext(request))
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
def reschedule_list_view2(request, appointment_id):
    print "aaaaaaa"
    if request.user.is_authenticated():
        schedule_date = request.POST['rebookingdate']
        appointment = Appointment.objects.get(id = appointment_id)
        print schedule_date
        errors = []
        if len(schedule_date) == 0:
            errors.append('date cannot be empty')
            return render_to_response('receptionist/patient-reschedule-2.htm',{'errors':errors, 'appointment':appointment}, context_instance=RequestContext(request))
        
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
        return render_to_response('receptionist/patient-reschedule-2.htm',{'dic':sorted_x, 'appointment':appointment}, context_instance=RequestContext(request))
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    

def reschedule_action2(request, schedule_id, appointment_id):
    if request.user.is_authenticated():
        errors = []
        if not Schedule.objects.filter(id = schedule_id).exists():
            errors.append('Schedule is not available')
            return render_to_response('receptionist/patient-reschedule-2.htm',{'errors':errors}, context_instance=RequestContext(request))
        
        print "haha"
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
        return redirect('main.views.receptionist.patients_view')    
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
    
    
    
def reschedule_view(request, appointment_id):
    if request.user.is_authenticated():
        if not Appointment.objects.filter(id = appointment_id).exists():
            return render_to_response('error.htm',{'error': "appointment is not exist"}, context_instance=RequestContext(request))
        appointment = Appointment.objects.get(id = appointment_id)
        print "aaaa"
        return render_to_response('receptionist/patient-reschedule.htm',{'appointment':appointment}, context_instance=RequestContext(request))
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
def reschedule_list_view(request, appointment_id):
    print "aaaaaaa"
    if request.user.is_authenticated():
        schedule_date = request.POST['rebookingdate']
        appointment = Appointment.objects.get(id = appointment_id)
        print schedule_date
        errors = []
        if len(schedule_date) == 0:
            errors.append('date cannot be empty')
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
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    

def reschedule_action(request, schedule_id, appointment_id):
    if request.user.is_authenticated():
        errors = []
        if not Schedule.objects.filter(id = schedule_id).exists():
            errors.append('Schedule is not available')
            return render_to_response('receptionist/patient-reschedule.htm',{'errors':errors}, context_instance=RequestContext(request))
        
        print "haha"
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
        return redirect('main.views.receptionist.patients_view')    
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))