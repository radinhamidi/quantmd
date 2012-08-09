from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.template import loader, Context
from django.views.decorators.csrf import csrf_exempt
from main.models.account import *
from main.models.appointment import Appointment 
from main.models.case import Case
from main.models.patient import Patient
from main.models.data import MRIData
from main.models.message import Message
from main.utils.misc import generate_random_string
from main.utils.form_check import *
from os import listdir, makedirs, rename
from os.path import isfile, join
from subprocess import call
from zipfile import ZipFile
import sys

def cardiologist(request):
    """Show lists of cardiologist"""
    
    
    return render_to_response('quantmd/cardilogist.htm', {},
                                  context_instance=RequestContext(request))



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
    """Create logs list view"""
    if request.user.is_authenticated():
        cases = Case.objects.all()
        return render_to_response('quantmd/logs.htm',{'cases':cases}, context_instance=RequestContext(request))     
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))


    
    
    