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
from main.models.mri import MRICenter
from main.models.case import Case
from main.utils.misc import generate_random_string
from main.utils.form_check import *
from main.models.appointment import Appointment
from main.models.analysis import Analysis

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
    case = Case.objects.get(pk=case_id)
    return render_to_response('quantmd/process-case.htm', {'case':case},
                                  context_instance=RequestContext(request))


def process_case_action(request):
    content = request.POST['diagnosis']
    analysis = Analysis(content=content)
    analysis.admin_id = request.user.pk
    analysis.save()
    
    case_id = request.POST['case_id']
    case = Case.objects.get(pk=case_id)
    case.analysis = analysis
    case.status = 3
    case.save()
    
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
        phone = request.POST['phone']
        address = request.POST['address']
        address2 = request.POST['address2']
        state = request.POST['state']
        zip = request.POST['zip']
        city = request.POST['city']
        error = []  
        print 'here1'
        # check form
        if IsEmpty(name):
            error.append('Name is empty')
        if IsEmpty(email) or not IsEmail(email):
            error.append('First name is empty or incorrect format')
        if IsEmpty(phone) or not phone.isdigit():
            error.append('Phone is empty or incorrect format')
        if IsEmpty(address):
            error.append('Address is empty')
        if IsEmpty(state):
            error.append('State is empty')
        if IsEmpty(zip) or not zip.isdigit():
            error.append('Zip is empty or incorrect format')
        if IsEmpty(city):
            error.append('City is empty') 
            
        if len(name) > 40:
            error.append('First name is too long')
        if IsEmpty(email) > 30:
            error.append('Email address is too long')
        if len(address) > 20:
            error.append('Address is too long')
        if IsEmpty(city) > 20:
            error.append('City is too long')
        
        if MRICenter.objects.filter(name=name).exists():
            error.append('There is a same name MRI center in quantmd')
        
        if len(error) != 0:
            return render_to_response('quantmd/mri-create.htm',{'errors':error},context_instance=RequestContext(request))
        else:
            city = city.upper()
            mri = MRICenter.objects.create(name=name,address=address,phone=phone,email=email,state=state,city=city,zip=zip)
            if len(address2) != 0:
                mri.address2 =address2
            mri.save()
            return render_to_response('quantmd/mri-create-confirm.htm',{'mri':mri}, context_instance=RequestContext(request))   
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
