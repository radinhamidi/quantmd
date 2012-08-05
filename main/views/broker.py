from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.template import loader, Context
from django.views.decorators.csrf import csrf_exempt
from main.models.account import *
from main.utils.misc import generate_random_string
import os
from subprocess import call
import sys


def upload(request):
    return render_to_response('broker/upload.htm', {},
                                  context_instance=RequestContext(request))
@csrf_exempt   
def upload_action(request):
    """
    Upload file and convert to images
    """
    try:
        uploaded = request.FILES['Filedata']
        print request.POST['test']
        f_name = generate_random_string() #server as both dir name and file names
        
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
        
        return HttpResponse('1')
    except Exception, e:
        return HttpResponse(str(e))


    
    