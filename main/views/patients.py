from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import *
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib import messages
from django.core.validators import email_re
from main.models.account import *
from main.models.patient import *
from main.models.appointment import *
from main.models.mri import *
from datetime import *
from main.utils.form_check import *
from main.models.case import *
from main.models.data import *
from main.models.message import *
from os import listdir, makedirs, rename
from os.path import isfile, join
import operator


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
    if request.user.is_authenticated():
        if Patient.objects.filter(id = patient_id).exists():
            patient = Patient.objects.get(id = patient_id)
            appointments = Appointment.objects.filter(patient=patient).filter(is_current=True).order_by('-case')
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
        # check form
        try:
            phone = long(request.POST['phone'])
            zip = int(request.POST['zip'])    
        except:
            messages.error(request, 'Phone and zipcode must be numbers')
            return redirect('main.views.patients.createView') 
        
        if (not first_name.strip() or not last_name.strip() or not email.strip() 
            or not address.strip() or not city.strip() or not state.strip()):
            messages.error(request, 'Only middle name and address line 2 can be empty.')
            return redirect('main.views.patients.createView') 
        if not email_re.match(email):
            messages.error(request, 'Email format not correct.')
            return redirect('main.views.patients.createView') 
        
        if ssn.strip() and not IsSSN(ssn):
            messages.error(request, 'SSN not correct.')
            return redirect('main.views.patients.createView')
        
        if not IsDate(birthday):
            messages.error(request, 'Birthday format not correct.')
            return redirect('main.views.patients.createView')
       
        format="%m/%d/%Y"
        doctor = Profile.objects.get(user=request.user)
        birthday_date = datetime.strptime(birthday,format)
        city = city.upper()
        patient = Patient.objects.create(first_name=first_name,middle_name=middle_name,last_name=last_name,gender=gender,address=address,phone=phone,
                                             email=email,state=state,city=city,zip=zip,birthday=birthday_date,doctor=doctor)
        if ssn:
            patient.ssn = ssn
        if address2:
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
        patient = Patient.objects.get(id=patient_id)
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
        try:
            phone = long(request.POST['phone'])
            zip = int(request.POST['zip'])    
        except:
            messages.error(request, 'Phone and zipcode must be numbers')
            return redirect('main.views.patients.patient_edit_view') 
        
        if (not first_name.strip() or not last_name.strip() or not email.strip() 
            or not address.strip() or not city.strip() or not state.strip()):
            messages.error(request, 'Only middle name and address line 2 can be empty.')
            return redirect('main.views.patients.patient_edit_view') 
        
        if not email_re.match(email):
            messages.error(request, 'Email format not correct.')
            return redirect('main.views.patients.patient_edit_view') 
        
        if ssn.strip() and not IsSSN(ssn):
            messages.error(request, 'SSN not correct.')
            return redirect('main.views.patients.patient_edit_view') 
        
        if not IsDate(birthday):
            messages.error(request, 'Birthday format not correct.')
            return redirect('main.views.patients.patient_edit_view') 
       
            
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
        if ssn:
            patient.ssn = ssn
        if address2:
            patient.address2 =address2
        patient.save()
        date = datetime.now()
         
        return render_to_response('referring/patient-edit-confirm.htm',{'patient':patient, 'date':date}, context_instance=RequestContext(request))
        
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

def view_mri_images(request, case_id):
    case = Case.objects.get(pk=case_id)
    data = case.data
    sequences = DataSequence.objects.filter(data=data)
    comments = Comment.objects.filter(data=data)
    comments_dict = {}
    for c in comments:
        comments_dict[c.image_index] = c.content
    image_objs = []
    for i in xrange(data.image_count):
        index = i + 1
        for s in sequences:
            if index >= s.image_start and index <= s.image_end:
                image_objs.append((index, str(index)+'.dcm.png', s.name, comments_dict.get(index, '')))
                break #found service name, continue to next image
        
    return render_to_response('referring/view-mri.htm', 
                              {'case':case, 'data':data, 'image_objs':image_objs},
                              context_instance=RequestContext(request))
    
def view_analysis(request, case_id):
    case = Case.objects.get(pk=case_id)
    data = case.data
    analysis = case.analysis
    directory = settings.MEDIA_ROOT + 'dicom/' + data.name + '/analysis'
    file_names = [ f for f in listdir(directory) if isfile(join(directory,f)) ]
    anal_videos = []
    anal_images = []
    for fn in file_names:
        if fn.lower().endswith('.mp4'):
            anal_videos.append(fn)
        else:
            anal_images.append(fn)
    
    return render_to_response('referring/view-analysis.htm', 
                              {'case':case, 'data':data, 'analysis':analysis, 'anal_videos':anal_videos,
                               'anal_images':anal_images},
                              context_instance=RequestContext(request))
    


