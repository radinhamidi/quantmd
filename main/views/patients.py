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
from main.models.data import *

# patients list
def patientsList(request):
    print "patientsList"
    if request.user.is_authenticated():
        profile = Profile.objects.get(user=request.user)
        print profile
        doctorAndPatients = PatientAndDoctor.objects.filter(doctor = profile)
        print doctorAndPatients
        dic = {}
        for doctorAndPatient in doctorAndPatients:
            patient = doctorAndPatient.patient
            appointments = Appointment.objects.filter(patient=patient)
            if len(appointments) != 0 :
                case = Case.objects.get(appointment=appointments[0])
                max_time = case.create_time
                for appointment in appointments:
                    case = Case.objects.get(appointment=appointment)
                    if case.status == 2:
                        time = case.data.create_time
                    elif case.status == 4:
                        time = case.report.create_time
                    else:
                        time = case.create_time
                    
                    if time > max_time:
                        max_time = time
                dic[patient] = max_time
            else:
                dic[patient] = 'N/A'
        print dic
        return render_to_response('referring/patients.htm',{'dic': dic}, context_instance=RequestContext(request)) 
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
            return render_to_response('referring/patient-info.htm',{'patient': patient, 'age': age}, context_instance=RequestContext(request)) 
        else:
            return HttpResponse('{"code":"0","msg":"No such patient"}')
    else: 
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))    
    
#e.g. if length>9....    
def createView(request):
    if request.user.is_authenticated():
        return render_to_response('referring/create-patient-ssn.htm', {},
                              context_instance=RequestContext(request))
    
    return render_to_response('login.htm',{}, context_instance=RequestContext(request))


def check_ssn(request):
    if request.user.is_authenticated():
        ssn = request.POST['ssn']
        print ssn
        error = []
        if IsEmpty(ssn) or not ssn.isdigit():
            error.append('SSN is empty ')
        if not IsSSN(ssn):
            error.append('SSN is not valid')
        if len(error) != 0:
            return render_to_response('referring/create-patient-ssn.htm',{'error':error},context_instance=RequestContext(request))
        
        if Patient.objects.filter(ssn=ssn).exists():
            patient = Patient.objects.get(ssn=ssn)
            doctor = Profile.objects.get(user=request.user)
            if PatientAndDoctor.objects.filter(patient=patient).filter(doctor=doctor).exists():
                error.append("This patient already belongs to you")
                return render_to_response('referring/create-patient-ssn.htm',{'error':error},context_instance=RequestContext(request))
            else:
                return render_to_response('referring/create-patient-link.htm', {'patient':patient}, context_instance=RequestContext(request))
        else:
            return render_to_response('referring/create-patient.htm', {'ssn':ssn}, context_instance=RequestContext(request))
           
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
def ssn_link(request,ssn):
    if request.user.is_authenticated():
        error = []
        if IsEmpty(ssn) or not ssn.isdigit():
            error.append('SSN is empty or incorrect format')
        if len(error) != 0:
            return render_to_response('referring/create-patient-ssn.htm',{'error':error},context_instance=RequestContext(request))
        
        patient = Patient.objects.get(ssn=ssn)
        doctor = Profile.objects.get(user=request.user)
        doctor_and_patient = PatientAndDoctor.objects.create(patient = patient, doctor = doctor)
        doctor_and_patient.save()
        
        return HttpResponseRedirect("/referring/patientsInfo/")
        
           
    else:
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
        address2 = request.POST['address']
        state = request.POST['state']
        zip = request.POST['zip']
        city = request.POST['city']
        print ssn
        error = []
        print "here1"   
        #if Patient.objects.filter(ssn=ssn).exists():
        #   error.append('Patient already exists')
        if IsEmpty(first_name):
            error.append('First name is empty')
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
            format="%m/%d/%Y"
            birthday_date = datetime.strptime(birthday,format)   
            patient = Patient.objects.create(ssn=ssn,first_name=first_name,middle_name=middle_name,last_name=last_name,gender=gender,address=address,address2=address2,phone=phone,
                                             state=state,city=city,zip=zip,birthday=birthday_date)  
            patient.save()
            doctor = Profile.objects.get(user=request.user)
            patient_and_doctor = PatientAndDoctor.objects.create(patient=patient,doctor=doctor)
            patient_and_doctor.save()
            return redirect("/referring/patientsInfo/")
            
    else: 
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    

def patient_appotiments(request, patient_ssn):
 if request.user.is_authenticated():
    print "patient apps"
    patient = Patient.objects.get(ssn=patient_ssn)
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
        return render_to_response('referring/Individual-diagnosis-list.htm', {'cases':cases, 'patient':patient},
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
        return render_to_response('referring/individual-diagnosis.htm', {'report':report, 'patient':patient, 'mri':mri},
                            context_instance=RequestContext(request))
    
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))    
    


