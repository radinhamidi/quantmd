from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import *
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from main.models.account import *
from main.models.patient import *
from main.models.appointment import *
from main.models.mri import *
from datetime import *
from main.utils.form_check import *
from main.models.case import *
from main.models.data import *
from main.models.message import *
import operator
from django.contrib.localflavor.it.util import ssn_check_digit


def patients_view(request):
    if request.user.is_authenticated():       
        return render_to_response('referring/patients.htm',{}, context_instance=RequestContext(request))
    else: 
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))    
# patients list
def patientsList(request):
    print "patientsList"
    if request.user.is_authenticated():
        profile = Profile.objects.get(user=request.user)
        patients = Patient.objects.filter(doctor = profile)
        print patients
        dic = {}
        for patient in patients:
            appointments = Appointment.objects.filter(patient=patient).filter(is_cancelled=False)
            dic[patient] = False
        print dic
        return render_to_response('referring/patient-list.htm',{'dic': dic}, context_instance=RequestContext(request)) 
    else: 
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    

# patient information   
def patientInfo(request, patient_id):
    print 'i am here'
    if request.user.is_authenticated():
        if Patient.objects.filter(id = patient_id).exists():
            patient = Patient.objects.get(id = patient_id)
            appointments = Appointment.objects.filter(patient=patient).filter(is_current=True).order_by('-case')
            print appointments
            return render_to_response('referring/patient-info.htm',{'patient': patient, 'appointments':appointments}, context_instance=RequestContext(request)) 
        else:
            return render_to_response('referring/error.htm',{'error': 'No such error'}, context_instance=RequestContext(request)) 
    else: 
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
#e.g. if length>9....    
def createView(request):
    if request.user.is_authenticated():
        return render_to_response('referring/patient-create.htm', {},
                              context_instance=RequestContext(request))
    
    return render_to_response('login.htm',{}, context_instance=RequestContext(request))

def createPatient(request):
    print 'wo lai le'
    if request.user.is_authenticated():
        first_name = request.POST['first_name']
        middle_name = request.POST['middle_name']
        ssn = request.POST['ssn']
        last_name = request.POST['last_name']
        gender = request.POST['sex']
        email = request.POST['email']
        birthday = request.POST['birthday']
        phone = request.POST['phone']
        address = request.POST['address']
        address2 = request.POST['address2']
        state = request.POST['state']
        zip = request.POST['zip']
        city = request.POST['city']
        error = []  
        print 'here1'
        # check form
        if IsEmpty(first_name):
            error.append('First name is empty')
        if IsEmpty(last_name):
            error.append('Last name is empty')
        if IsEmpty(email) or not IsEmail(email):
            error.append('First name is empty or incorrect format')
        if not IsEmpty(ssn) and not ssn.isdigit():
            error.append('SSN is incorrect format')
        if not IsEmpty(ssn) and not IsSSN(ssn):
            error.append('SSN is incorrect')
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
        if IsEmpty(birthday) or not IsDate(birthday):
            error.append('Birthday is empty or incorrect format')  
            
        if len(first_name) > 20:
            error.append('First name is too long')
        if len(last_name) > 20:
            error.append('Last name is too long')
        if IsEmpty(email) > 30:
            error.append('Email address is too long')
        if len(address) > 20:
            error.append('Address is too long')
        if IsEmpty(city) > 20:
            error.append('City is too long')
        

        if len(error) != 0:
            return render_to_response('referring/patient-create.htm',{'errors':error},context_instance=RequestContext(request))
        else:
            format="%m/%d/%Y"
            doctor = Profile.objects.get(user=request.user)
            birthday_date = datetime.strptime(birthday,format)
            city = city.upper()
            patient = Patient.objects.create(first_name=first_name,middle_name=middle_name,last_name=last_name,gender=gender,address=address,phone=phone,
                                             email=email,state=state,city=city,zip=zip,birthday=birthday_date,doctor=doctor)
            if len(ssn) != 0:
                patient.ssn = ssn
            if len(address2) != 0:
                patient.address2 =address2
            patient.save()
            return render_to_response('referring/patient-create-confirm.htm',{'patient':patient}, context_instance=RequestContext(request))
            
    else: 
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))


def patient_edit_view(request, patient_id):
    if request.user.is_authenticated():
        print "patient apps"
        patient = Patient.objects.get(id=patient_id)
        
        return render_to_response('referring/patient-edit.htm', {'patient':patient},
                        context_instance=RequestContext(request))
    
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))

def patient_edit_action(request, patient_id):
    if request.user.is_authenticated():
        first_name = request.POST['first_name']
        middle_name = request.POST['middle_name']
        ssn = request.POST['ssn']
        last_name = request.POST['last_name']
        gender = request.POST['sex']
        email = request.POST['email']
        birthday = request.POST['birthday']
        phone = request.POST['phone']
        address = request.POST['address']
        address2 = request.POST['address2']
        state = request.POST['state']
        zip = request.POST['zip']
        city = request.POST['city']
        print ssn
        error = []
        print "here1"   
         # check form
        if IsEmpty(first_name):
            error.append('First name is empty')
        if IsEmpty(last_name):
            error.append('Last name is empty')
        if IsEmpty(email) or not IsEmail(email):
            error.append('First name is empty or incorrect format')
        if not IsEmpty(ssn) and not ssn.isdigit():
            error.append('SSN is incorrect format')
        if not IsEmpty(ssn) and not IsSSN(ssn):
            error.append('SSN is incorrect')
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
        if IsEmpty(birthday) or not IsDate(birthday):
            error.append('Birthday is empty or incorrect format')  
            
        if len(first_name) > 20:
            error.append('First name is too long')
        if len(last_name) > 20:
            error.append('Last name is too long')
        if IsEmpty(email) > 30:
            error.append('Email address is too long')
        if len(address) > 20:
            error.append('Address is too long')
        if IsEmpty(city) > 20:
            error.append('City is too long')
        
        print "here2"
        if len(error) != 0:
            return render_to_response('referring/patient-edit.htm',{'errors':error},context_instance=RequestContext(request))
        else:
            print "here3"
            format="%m/%d/%Y"
            birthday_date = datetime.strptime(birthday,format)
            patient = Patient.objects.get(id=patient_id)
            patient.first_name = first_name
            patient.middle_name = middle_name
            patient.last_name = last_name
            patient.birthday = birthday_date
            patient.email = email
            patient.phone = phone
            patient.address = address
            patient.city = city
            patient.state = state
            patient.zip = zip
            if len(ssn) != 0:
                patient.ssn = ssn
            if len(address2) != 0:
                patient.address2 =address2
            patient.save()
            print "here4"
            return render_to_response('referring/patient-edit-confirm.htm',{'patient':patient}, context_instance=RequestContext(request))
        
    else: 
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))

def patient_appotiments(request, patient_id):
 if request.user.is_authenticated():
    print "patient apps"
    patient = Patient.objects.get(id=patient_id)
    appointments = Appointment.objects.filter(patient=patient)
    dic = {}
    for appointment in appointments:
        case = Case.objects.get(appointment=appointment)
        dic[appointment] = case
    print dic
    return render_to_response('referring/Individual-schedule-list.htm', {'dic': dic, 'patient':patient},
                            context_instance=RequestContext(request))
    
 else:
    return render_to_response('login.htm',{}, context_instance=RequestContext(request))


def patient_appotiment(request, schedule_id, patient_ssn):
    print "appointment"
    if request.user.is_authenticated():
        schedule = Schedule.objects.get(id=schedule_id)
        patient = Patient.objects.get(ssn=patient_ssn)
        appointment = Appointment.objects.get(schedule=schedule)
        mri = schedule.mri                        
        return render_to_response('referring/individual-schedule.htm', {'schedule':schedule, 'patient':patient, 'mri':mri, 'appointment':appointment},
                            context_instance=RequestContext(request))
    
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
    
def patient_cases(request, patient_id):
    print "cases"
    if request.user.is_authenticated():
        errors = []
        if Patient.objects.filter(id=patient_id):
            errors.append('Patient is not exist')
            return render_to_response('referring/Individual-diagnosis-list.htm', {'errors': errors},
                            context_instance=RequestContext(request))
        patient = Patient.objects.get(id=patient_id)
        appointments = Appointment.objects.filter(patient=patient).filter(is_cancelled=False)
        cases = {}
        for appointment in appointments:
            case = Case.objects.get(appointment=appointment)
            if case.report is not None:
                cases[case] = case.report 
        print cases                    
        return render_to_response('referring/Individual-diagnosis-list.htm', {'cases':cases, 'patient':patient},
                            context_instance=RequestContext(request))
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
      
def patient_case(request, case_id):
    if request.user.is_authenticated():
        if Case.objects.filter(id=case_id):
            case = Case.objects.get(id=case_id)
            appointment = Appointment.objects.filter(case=case).filter(is_current=True)[0]
            patient = appointment.patient
            messages = Message.objects.filter(case=case)
            
            return render_to_response('referring/case-view.htm', {'case':case, 'appointment':appointment, 'patient':patient, 'messages':messages},
                                      context_instance=RequestContext(request))
        else:
            return render_to_response('error.htm', {'error':"No such Case"},
                                      context_instance=RequestContext(request))
    
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))    
    


