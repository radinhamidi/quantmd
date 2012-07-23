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
from datetime import *
from main.utils.form_check import *
from main.models.case import *

# patients list
def patientsList(request):
    print "patientsList"
    if request.user.is_authenticated():
        patients = []
        profile = Profile.objects.get(user=request.user)
        doctorAndPatients = PatientAndDoctor.objects.filter(doctor = profile)
        for doctorAndPatient in doctorAndPatients:
            patient = doctorAndPatient.patient
            patients.append(patient)
        return render_to_response('referring/patients.htm',{'Patients': patients}, context_instance=RequestContext(request)) 
    else: 
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
    
# patient information   
def patientInfo(request, patient_ssn):
    print 'i am here'
    if request.user.is_authenticated():
        patient = Patient.objects.get(ssn = patient_ssn)        
        if patient is not None:
            age = datetime.now().year - patient.birthday.year
            print age
            return render_to_response('referring/patient-info.htm',{'Patient': patient, 'Age': age}, context_instance=RequestContext(request)) 
        else:
            return HttpResponse('{"code":"0","msg":"No such patient"}')
    else: 
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))    
    
    
def createView(request):
    if request.user.is_authenticated():
        return render_to_response('referring/create-patient.htm', {},
                              context_instance=RequestContext(request))
    
    return render_to_response('login.htm',{}, context_instance=RequestContext(request))

def createPatient(request):
    print 'wo lai le'
    if request.user.is_authenticated():
        first_name = request.POST['first_name']
        middle_name = request.POST['middle_name']
        last_name = request.POST['last_name']
        ssn = request.POST['ssn']
        gender = request.POST['sex']
        email = request.POST['email']
        birthday = request.POST['birthday']
        phone = request.POST['phone']
        address = request.POST['address']
        address2 = request.POST['address']
        state = request.POST['state']
        zip = request.POST['zip']
        city = request.POST['city']
        
        error = []
        print "here1"   
        if Patient.objects.filter(ssn=ssn).exists():
            error.append('Patient already exists')
        if IsEmpty(first_name):
            error.append('First name is empty')
        if IsEmpty(middle_name):
            error.append('Middle name is empty')
        if IsEmpty(last_name):
            error.append('Last name is empty')
        if IsEmpty(email):
            error.append('First name is empty or incorrect format')
        if IsEmpty(ssn) or not ssn.isdigit():
            error.append('SSN is empty or incorrect format')
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
         
        print "here0"   
        if len(error) != 0:
            return render_to_response('referring/create-patient.htm',{'error':error},context_instance=RequestContext(request))
        else:
            print "here2"
            format="%m/%d/%Y"
            birthday_date = datetime.strptime(birthday,format)   
            patient = Patient.objects.create(ssn=ssn,first_name=first_name,middle_name=middle_name,last_name=last_name,gender=gender,address=address,address2=address2,phone=phone,
                                             state=state,city=city,zip=zip,birthday=birthday_date)
            print "here3"   
            patient.save()
            doctor = Profile.objects.get(user=request.user)
            patient_and_doctor = PatientAndDoctor.objects.create(patient=patient,doctor=doctor)
            patient_and_doctor.save()
            return HttpResponseRedirect("/referring/patientsInfo/")
            
    else: 
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    

def patient_appotiments(request, patient_ssn):
 if request.user.is_authenticated():
    print "patient apps"
    patient = Patient.objects.get(ssn=patient_ssn)
    print patient
    appointments = Appointment.objects.filter(patient=patient)
    
    dic = {}
    for appointment in appointments:
        dic[appointment.schedule] = appointment.mri
    
    print dic                            
    return render_to_response('referring/Individual-schedule-list.htm', {'Dic': dic, 'Patient':patient},
                            context_instance=RequestContext(request))
    
 else:
    return render_to_response('login.htm',{}, context_instance=RequestContext(request))


def patient_appotiment(request, schedule_id, patient_ssn):
    print "appointment"
    if request.user.is_authenticated():
        schedule = Schedule.objects.get(id=schedule_id)
        patient = Patient.objects.get(ssn=patient_ssn)
        mri = schedule.mri                        
        return render_to_response('referring/individual-schedule.htm', {'Schedule':schedule, 'Patient':patient, 'MRI':mri},
                            context_instance=RequestContext(request))
    
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
    
def patient_cases(request, patient_ssn):
    print "cases"
    if request.user.is_authenticated():
        patient = Patient.objects.get(ssn=patient_ssn)
        appointments = Appointment.objects.filter(patient=patient)
        cases = {}
        for appointment in appointments:
            case = Case.objects.get(appointment=appointment)
            if case.report is not None:
                cases[case] = case.report 
        print cases                    
        return render_to_response('referring/Individual-diagnosis-list.htm', {'Cases':cases, 'Patient':patient},
                            context_instance=RequestContext(request))
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
      
def patient_case(request, case_id):
    print "case"
    if request.user.is_authenticated():
        case = Case.objects.get(id=case_id)
        report = case.report
        appointment = case.appointment
        patient = appointment.patient
        mri = appointment.mri                     
        return render_to_response('referring/individual-diagnosis.htm', {'Report':report, 'Patient':patient, 'MRI':mri},
                            context_instance=RequestContext(request))
    
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))    
    


