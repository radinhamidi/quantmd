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
import os
from subprocess import call
import sys


def patients(request):
    """Show lists of patients awaiting uploading of dicom file"""
    profile = Profile.objects.get(pk=request.user.pk)
    apts = Appointment.objects.filter(mri=profile.mri_id, case_status=1, 
                                      is_cancelled=False, is_current=True)
    
    mri_name = profile.mri_id.name
    return render_to_response('broker/patients.htm', {'apts':apts, 'mri_name':mri_name},
                                  context_instance=RequestContext(request))

def upload(request, patient_id, case_id):
    """The upload interface"""
    patient = Patient.objects.get(pk=patient_id)
    return render_to_response('broker/upload.htm', {'patient':patient, 'case_id':case_id},
                                  context_instance=RequestContext(request))


@csrf_exempt   
def upload_action(request):
    """
    Upload file and convert to images
    """
    try:
        uploaded = request.FILES['Filedata']
        f_name = generate_random_string(10) #serve as both dir name and file names
        
        #Create a folder holding dicom file and converted images
        directory = settings.MEDIA_ROOT + 'dicom/' + f_name
        os.makedirs(directory)
        
        #Write the dicom file
        f_path = directory + '/' + f_name + '.dcm'
        f = open(f_path, 'wb')
        f.write(uploaded.read())
        f.close()
        
        #Convert images
        LINUX = sys.platform.startswith('linux')
        MAC = sys.platform.startswith('darwin')
        WINDOWS = sys.platform.startswith('win32')
        if LINUX or MAC:
            call(settings.PROJECT_ROOT + 'main/utils/dicom2-unix ' + f_path + ' -w --to=' + directory)
        else:
            command = settings.PROJECT_ROOT + 'main/utils/dicom2-windows ' + f_path + ' -w --to=' + directory
            call(command)
        
        #Update database
        data = MRIData(name=f_name)
        data.broker_id = request.user.pk
        data.save()
        case_id = request.POST['case_id']
        case = Case.objects.get(pk=case_id)
        case.data = data
        case.status = 2
        case.save()
        
        
        apt = Appointment.objects.get(case=case_id, is_current=True)
        apt.case_status = case.status
        apt.save()
        
        #Send message to referring doctor to notify him that scan is complete and uploaded
        message = Message(is_sys=True, type=3, receiver=apt.doctor, case=case)
        message.title = 'MRI scan complete for ' + case_id
        message.content = 'The MRI scan is complete for case ' + case_id \
                          + '. Please wait for cardiologist to upload report' 
        message.save()
        return HttpResponse('0')
    except Exception, e:
        return HttpResponse(str(e))


    
    