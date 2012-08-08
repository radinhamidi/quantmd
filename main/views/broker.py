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
from os import listdir, makedirs, rename
from os.path import isfile, join
from subprocess import call
import sys


def patients(request):
    """Show lists of patients awaiting uploading of dicom file"""
    profile = Profile.objects.get(pk=request.user.pk)
    apts = Appointment.objects.filter(mri=profile.mri_id, case__status=1, 
                                      is_cancelled=False, is_current=True)
    
    mri_name = profile.mri_id.name
    
    return render_to_response('broker/patients.htm', {'apts':apts, 'mri_name':mri_name},
                                  context_instance=RequestContext(request))

def upload(request, patient_id, case_id):
    """The upload interface"""
    patient = Patient.objects.get(pk=patient_id)
    identifier = generate_random_string(10)
    return render_to_response('broker/upload.htm', {'patient':patient, 'case_id':case_id,
                                                    'identifier':identifier},
                                  context_instance=RequestContext(request))


@csrf_exempt   
def upload_action(request):
    """
    Upload file and convert to images
    """
    try:
        uploaded = request.FILES['Filedata']
        identifier = request.POST['identifier']
        
        #Create a folder holding dicom file and converted images
        directory = settings.MEDIA_ROOT + 'dicom/' + identifier
        try:
            makedirs(directory) #makes all intermediary dir if necessary
        except: #dir exist, just store
            pass
        
        #Write the dicom file
        f_path = directory + '/' + uploaded.name
        f = open(f_path, 'wb')
        f.write(uploaded.read())
        f.close()
        
        return HttpResponse('0')
    except Exception, e:
        return HttpResponse(str(e))
    
@csrf_exempt 
def upload_complete(request):
    try:
        identifier = request.POST['identifier']
        case_id = request.POST['case_id']
        
        directory = settings.MEDIA_ROOT + 'dicom/' + identifier
        file_names = [ f for f in listdir(directory) if isfile(join(directory,f)) ]
        file_names.sort()
        image_count = 0
        for fn in file_names:
            f_path = join(directory,fn)
            new_path = join(directory,str(image_count+1)+'.dcm')
            rename(f_path, new_path)
            #Convert images
            LINUX = sys.platform.startswith('linux')
            MAC = sys.platform.startswith('darwin')
            WINDOWS = sys.platform.startswith('win32')
            if LINUX or MAC:
                call(settings.PROJECT_ROOT + 'main/utils/dicom2-unix ' + new_path + 
                     ' -p --to=' + directory + ' --rename=cur_nm')
            else:
                call(settings.PROJECT_ROOT + 'main/utils/dicom2-windows ' + new_path +
                         ' -p --to=' + directory + ' --rename=cur_nm')
            image_count += 1
        
        #Update database
        data = MRIData(name=identifier)
        data.image_count = image_count 
        data.broker_id = request.user.pk
        data.save()
        
        case_id = request.POST['case_id']
        case = Case.objects.get(pk=case_id)
        case.data = data
        case.status = 2
        case.save()
           
        apt = Appointment.objects.get(case=case_id, is_current=True)
        apt.save()
        
        #Send message to referring doctor to notify him that scan is complete and uploaded
        message = Message(is_sys=True, type=3, receiver=apt.doctor, case=case)
        message.title = 'MRI scan complete for ' + case_id
        message.content = 'The MRI scan is complete for case ' + case_id \
                          + '. Please wait for cardiologist to upload report' 
        message.save()
        return HttpResponse('{"code":"0", "msg":"Completed!"}')
    except:
        return HttpResponse('{"code":"1", "msg":"Error while processing dicom files."}')
    


def logs(request):
    """The logs of uploaded files"""
    profile = Profile.objects.get(pk=request.user.pk)
    apts = Appointment.objects.filter(mri=profile.mri_id, case__status__gte=2, 
                                      is_cancelled=False, is_current=True)
    return render_to_response('broker/logs.htm', {'apts':apts},
                                  context_instance=RequestContext(request))



    
    