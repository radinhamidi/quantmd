from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.template import loader, Context
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from main.models.account import *
from django.core.validators import email_re
from main.models.mri import *
from main.models.case import Case,Service
from main.utils.misc import generate_random_string
from main.utils.form_check import *
from main.models.appointment import Appointment
from main.models.analysis import Analysis
from main.utils.date_process import *
from main.models.report import *
import datetime
import operator
import time
from os import listdir, makedirs, rename
from os.path import isfile, join
from subprocess import call
from zipfile import ZipFile
import sys

def create_user(request, role):
    mris = MRICenter.objects.all()
    return render_to_response('quantmd/create-user.htm', {'mris':mris, 'role':role},
                                  context_instance=RequestContext(request))

def create_user_action(request):
    username = request.POST['username']
    password = request.POST['password']
    password_confirm = request.POST['password_confirm']
    first_name = request.POST['first_name']
    middle_name = request.POST['middle_name']
    last_name = request.POST['last_name']
    gender = request.POST['gender']
    email = request.POST['email']
    address = request.POST['address']
    address_2 = request.POST['address_2']
    city = request.POST['city']
    state = request.POST['state']
    role = int(request.POST['role'])
    mri_id = int(request.POST['mri']) if 'mri' in request.POST else None
    try:
        phone = long(request.POST['phone'])
        zip = int(request.POST['zipcode'])    
    except:
        messages.error(request, 'Phone and zipcode must be numbers')
        return redirect('main.views.quantmd.create_user') 
        
    
    if not password.strip() or password != password_confirm:
        messages.error(request, 'Password is empty or does not match')
        return redirect('main.views.quantmd.create_user')      
    if not username.strip():
        messages.error(request, 'Username cannot be empty')
        return redirect('main.views.quantmd.create_user')
    user, created = User.objects.get_or_create(username=username)
    if not created:
        messages.error(request, 'Username already exists!')
        return redirect('main.views.quantmd.create_user')
    user.set_password(password)
    user.save()
    
    if (not first_name.strip() or not last_name.strip() or not email.strip() 
        or not address.strip() or not city.strip() or not state.strip()): 
        messages.error(request, 'Only middle name and address line 2 can be empty.')
        return redirect('main.views.quantmd.create_user')
    if not email_re.match(email):
        messages.error(request, 'Email format not correct.')
        return redirect('main.views.quantmd.create_user')
    
    profile = Profile(user=user, first_name=first_name, middle_name=middle_name,
                      last_name=last_name, gender=int(gender), email=email, phone=phone,
                      address=address, address2=address_2, city=city, state=state,
                      zip=zip, role=role)
    if mri_id:
        profile.mri_id_id = mri_id
    profile.save()
    
    messages.info(request, 'Successfully created the user')
    return redirect('main.views.quantmd.create_user')
        
def edit_user(request, user_id):
    profile = Profile.objects.get(pk=user_id)
    mris = MRICenter.objects.all()
    return render_to_response('quantmd/edit-user.htm', {'profile':profile, 'mris':mris},
                                  context_instance=RequestContext(request))

def edit_user_action(request):
    user_id = request.POST['user_id']
    p = Profile.objects.get(pk=user_id) 
    
    first_name = request.POST['first_name']
    middle_name = request.POST['middle_name']
    last_name = request.POST['last_name']
    gender = int(request.POST['gender'])
    email = request.POST['email']
    address = request.POST['address']
    address_2 = request.POST['address_2']
    city = request.POST['city']
    state = request.POST['state']
    mri_id = int(request.POST['mri']) if 'mri' in request.POST else None
    try:
        phone = long(request.POST['phone'])
        zip = int(request.POST['zipcode'])    
    except:
        messages.error(request, 'Phone and zipcode must be numbers')
        return redirect('main.views.quantmd.create_user') 
        
    if (not first_name.strip() or not last_name.strip() or not email.strip() 
        or not address.strip() or not city.strip() or not state.strip()): 
        messages.error(request, 'Only middle name and address line 2 can be empty.')
        return redirect('main.views.quantmd.create_user')
    if not email_re.match(email):
        messages.error(request, 'Email format not correct.')
        return redirect('main.views.quantmd.create_user')
    
    p.first_name = first_name
    p.middle_name = middle_name
    p.last_name = last_name
    p.gender = gender
    p.email = email
    p.address = address
    p.address2 = address_2
    p.phone = phone
    p.zip = zip
    p.city = city
    p.state = state
    if mri_id:
        p.mri_id_id = mri_id
    p.save()
    
    messages.info(request, 'Saved changes to user information.')
    return redirect('main.views.quantmd.edit_user', str(p.pk))

def view_user(request, user_id):
    user = User.objects.get(pk=user_id)
    profile = Profile.objects.get(pk=user_id)
    return render_to_response('quantmd/view-user.htm', {'user':user, 'profile':profile},
                                  context_instance=RequestContext(request))


def doctors(request):
    """Show lists of doctors"""
    profiles = Profile.objects.filter(role=1)
    return render_to_response('quantmd/doctors.htm', {'profiles':profiles},
                                  context_instance=RequestContext(request))

def receptionists(request):
    """Show lists of receptionists"""
    profiles = Profile.objects.filter(role=2)
    return render_to_response('quantmd/receptionists.htm', {'profiles':profiles},
                                  context_instance=RequestContext(request))

def brokers(request):
    """Show lists of brokers"""
    profiles = Profile.objects.filter(role=3)
    return render_to_response('quantmd/brokers.htm', {'profiles':profiles},
                                  context_instance=RequestContext(request))
    
    
def cardiologists(request):
    """Show lists of cardiologist"""
    profiles = Profile.objects.filter(role=4)
    return render_to_response('quantmd/cardiologists.htm', {'profiles':profiles},
                                  context_instance=RequestContext(request))

def process_cases(request):
    """Show a list of cases that need private algorithm to process"""
    cases = Case.objects.filter(status=2)
    return render_to_response('quantmd/process-cases.htm', {'cases':cases},
                                  context_instance=RequestContext(request))


def process_case(request, case_id):
    """Show interfae of process one case"""
    case = Case.objects.get(pk=case_id)
    return render_to_response('quantmd/process-case.htm', {'case':case},
                                  context_instance=RequestContext(request))


@csrf_exempt   
def upload_action(request):
    """
    Upload files, only mp4 and images are allowed
    """
    try:
        uploaded = request.FILES['Filedata']
        case_id = request.POST['case_id']
        case = Case.objects.get(pk=case_id)
        
        extentions = ['.mp4', '.jpg', '.jpeg', '.png', '.gif']
        extentions2 = [s.upper() for s in extentions]
        extentions.extend(extentions2)
        dot_index = uploaded.name.rfind('.')
        if uploaded.name[dot_index:] not in extentions:
            return HttpResponse('Only mp4 and image files can be uploaded.')
        
        #Create a folder holding analysis files
        directory = settings.MEDIA_ROOT + 'dicom/' + case.data.name + '/analysis'
        try:
            makedirs(directory) #makes all intermediary dir if necessary
        except: #dir exist, just store
            pass
        
        #Write the file
        f_path = directory + '/' + uploaded.name
        f = open(f_path, 'wb')
        f.write(uploaded.read())
        f.close()
        
        return HttpResponse('0')
    except Exception, e:
        return HttpResponse(str(e))

@csrf_exempt
def process_case_action(request):
    """Store the files in 'analysis' folder and save analysis"""
    analysis.admin_id = request.user.pk
    analysis.save()
    
    case_id = request.POST['case_id']
    case = Case.objects.get(pk=case_id)
    case.analysis = analysis
    case.status = 3
    case.save()
    
    appointment = Appointment.objects.filter(case = case, is_current = True, is_cancelled = False)[0]
    
    title = 'Analysis is available for CASE #' + str(case.id) 
    title = title.upper()
     
    content = 'Analysis is available for CASE #: ' + str(case.id)
        # content = "You have already made an appointment"
        
    message = Message.objects.create(receiver = appointment.doctor, case = case, title = title, content = content, type = 2, is_sys = True)
    message.save()
        
    
    messages.info(request, 'Successfully submited diagnosis of case.')
    return redirect('main.views.quantmd.process_cases')
    


#Yang xie's code below this line:
def mri(request):
    """Show lists of mri center"""
    if request.user.is_authenticated():
        mris = MRICenter.objects.all()
        mri_centers = {}
        for mri in mris:
            case_count = Appointment.objects.filter(mri = mri, is_current=True).count()
            mri_centers[mri] = case_count
        print mri_centers
        return render_to_response('quantmd/mri.htm',{'mri':mri_centers}, context_instance=RequestContext(request))     
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
def mri_view(request,mri_id):
    """Show mri detail"""
    if request.user.is_authenticated():
        mri = MRICenter.objects.get(id = mri_id)
        profiles = Profile.objects.filter(mri_id = mri)
        return render_to_response('quantmd/mri-view.htm',{'mri':mri, 'profiles':profiles}, context_instance=RequestContext(request))     
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))

def mri_schedule(request, mri_id, month):
    print "heiheihei"
    if request.user.is_authenticated():
        mri = MRICenter.objects.get(id = mri_id)
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
        return render_to_response('quantmd/mri-schedule.htm',{'dic':sorted_x, 'date': date, 'month': month, 'mri':mri}, context_instance=RequestContext(request))  
    else: 
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))

    
    
def create_mri_view(request):
    """Create mri center view"""
    if request.user.is_authenticated():
        return render_to_response('quantmd/mri-create.htm',{}, context_instance=RequestContext(request))     
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))


def create_mri_action(request):
    if request.user.is_authenticated():
        name = request.POST['name']
        email = request.POST['email']
        address = request.POST['address']
        address2 = request.POST['address2']
        state = request.POST['state']
        city = request.POST['city']
        
        try:
            phone = long(request.POST['phone'])
            zip = int(request.POST['zipcode'])    
        except:
            messages.error(request, 'Phone and zipcode must be numbers')
            return redirect('main.views.quantmd.create_mri_view') 
        
        if (not name.strip() or not email.strip() or not address.strip() or not city.strip() or not state.strip()): 
            messages.error(request, 'Only address line 2 can be empty.')
            return redirect('main.views.quantmd.create_mri_view')
        
        if not email_re.match(email):
            messages.error(request, 'Email format not correct.')
            return redirect('main.views.quantmd.create_mri_view')
    
        if MRICenter.objects.filter(name=name).exists():
            messages.error('There is a same name MRI center in quantmd')
            return redirect('main.views.quantmd.create_mri_view')
        
        city = city.upper()
        mri = MRICenter.objects.create(name=name,address=address,phone=phone,email=email,state=state,city=city,zip=zip)
        if len(address2) != 0:
            mri.address2 =address2
            
        mri.save()
        return render_to_response('quantmd/mri-create-confirm.htm',{'mri':mri}, context_instance=RequestContext(request))
    
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
def edit_mri_view(request, mri_id):
    if request.user.is_authenticated():
        mri = MRICenter.objects.get(id = mri_id)
        return render_to_response('quantmd/mri-edit.htm',{'mri':mri}, context_instance=RequestContext(request))     
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))

def edit_mri_action(request):
    if request.user.is_authenticated():
        mri_id = request.POST['mri_id']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        address2 = request.POST['address2']
        state = request.POST['state']
        zip = request.POST['zip']
        city = request.POST['city']
        
        try:
            phone = long(request.POST['phone'])
            zip = int(request.POST['zipcode'])    
        except:
            messages.error(request, 'Phone and zipcode must be numbers')
            return redirect('main.views.quantmd.edit_mri_view') 
        
        if (not name.strip() or not email.strip() or not address.strip() or not city.strip() or not state.strip()): 
            messages.error(request, 'Only address line 2 can be empty.')
            return redirect('main.views.quantmd.edit_mri_view')
        
        if not email_re.match(email):
            messages.error(request, 'Email format not correct.')
            return redirect('main.views.quantmd.edit_mri_view')
        
        mri = MRICenter.objects.get(id = mri_id)
        city = city.upper()
        mri.name = name
        mri.email = email
        mri.phone = phone
        mri.address = address
        mri.address2 = address2
        mri.state = state
        mri.zip = zip
        mri.city = city
            
        if address2.strip() != 0:
            mri.address2 =address2
        mri.save()
        return render_to_response('quantmd/mri-edit-confirm.htm',{'mri':mri}, context_instance=RequestContext(request))   
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
        
def logs_view(request):
    """logs list view"""
    if request.user.is_authenticated():
        appointments = Appointment.objects.filter(is_current = True).order_by('-create_time')
        return render_to_response('quantmd/logs.htm',{'appointments':appointments}, context_instance=RequestContext(request))     
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    

def log_view(request, case_id):
    """logs view"""
    if request.user.is_authenticated():
        case = Case.objects.get(id=case_id)
        appointments = Appointment.objects.filter(case = case, is_current = True)
        return render_to_response('quantmd/log-view.htm',{'appointment':appointments[0], 'case':case}, context_instance=RequestContext(request))     
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
def dashborad(request):
    if request.user.is_authenticated():
        monday = get_monday()
        unprocess_count = Case.objects.filter(status=2).count()
        complete_count = Report.objects.filter(create_time__gte= monday).count()
        awiting_dia_count = Case.objects.filter(status=3).count() + Case.objects.filter(status=4).count()
        schedule_count = Appointment.objects.filter(create_time__gte= monday, is_current=True, is_cancelled=False).count()
        
        doctors = Profile.objects.raw("select p.* from main_profile as p, main_appointment as apt \
                        where apt.is_current = 1 and apt.is_cancelled = 0 and apt.doctor_id = p.user_id\
                        and apt.create_time > '%s' group by apt.doctor_id \
                        order by count(apt.doctor_id) desc limit 0,5" % monday)
        doctors = list(doctors)

        for i in xrange(len(doctors)):
            doctors[i].count = Appointment.objects.filter(doctor=doctors[i],create_time__gte= monday, is_current=True, is_cancelled=False).count()
        
        cases = Case.objects.filter(assigned_time__gte= monday)
        print monday
        print cases
        cardi_counts = {}
        for c in cases:
            if c.cardiologist_id:
                if c.cardiologist_id in cardi_counts:
                    cardi_counts[c.cardiologist_id] += 1
                else:
                    cardi_counts[c.cardiologist_id] = 1
        sorted_d = sorted(cardi_counts.iteritems(), key=operator.itemgetter(1), reverse=True)
        cardi_ids = [i[0] for i in sorted_d[:5]]
        
        cardiologists = Profile.objects.filter(pk__in=cardi_ids)
        for i in xrange(len(cardiologists)):
            cardiologists[i].count = cardi_counts[cardiologists[i].pk]
        
        return render_to_response('quantmd/dashboard.htm',{"unprocess":unprocess_count, 'complete':complete_count, 'awiting':awiting_dia_count, 
                                                           'schedule':schedule_count, "doctors":doctors,
                                                           'cardiologists':cardiologists, }, 
                                   context_instance=RequestContext(request))     
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
def services_view(request):
    if request.user.is_authenticated():
        services = Service.objects.all()
        return render_to_response('quantmd/services.htm',{'services':services}, context_instance=RequestContext(request))     
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
def services_stop(request, service_id):
    if request.user.is_authenticated():
        service = Service.objects.get(id=service_id)
        service.is_active = False
        service.save()
        return redirect('main.views.quantmd.services_view')    
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
def services_active(request,service_id):
    if request.user.is_authenticated():
        service = Service.objects.get(id=service_id)
        service.is_active = True
        service.save()
        return redirect('main.views.quantmd.services_view')    
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
def services_add(request):
    if request.user.is_authenticated():
        name = request.POST['add-scan-name']
        if not name.strip():
            messages.error(request, 'Service name cannot be empty')
            return redirect('main.views.quantmd.services_view') 
        
        service = Service.objects.create(name=name)
        service.save()
        return redirect('main.views.quantmd.services_view')    
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
